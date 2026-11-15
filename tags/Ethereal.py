import LevelRewards
import Game
import ModHandler
import sys
from Level import Color, EventOnMoved, EventOnUnitAdded, Level, Portal, Tag, Tags, TEAM_PLAYER

from RareMonsters import SlimeAdaptiveArmorBuff
from mods.EtherealPack.models.hazards.base import EtherealHazard
import mods.EtherealPack.models.hazards.layer

#TODO staff with minion health / number
#TODO staff with damage, range and minion damage, range 4 3 4 3
#TODO make euqipment staff that gives bonus charges and duration
#TODO make icons animated again!
#TODO ethermancer trial give ethermancer robe
#TODO make spells/equipment scale with appropiate spell bonuses where not already done. Mostly missing for upgrades / equipment
#TODO Rework vanilla ether spider
Ethereal = ModHandler.register_tag("Äthereal", Color(1, 255, 188), letter="v", asset=["EtherealPack", "ether"])
Etherealness = Tag("Ätherealness", Color(1, 255, 188))


def on_unit_added(evt):
    unit = evt.unit

    if Tags.Arcane in unit.tags:
        unit.resists[Ethereal] += 25

        if unit.max_hp > 29:
            unit.resists[Ethereal] += 25

            if unit.max_hp > 99:
                unit.resists[Ethereal] += 25

    if Tags.Holy in unit.tags or Tags.Dark in unit.tags:
        unit.resists[Ethereal] -= 50


def on_unit_moved(evt):
    tile = evt.unit.level.tiles[evt.x][evt.y]
    for hazard in list(getattr(tile, "hazards", ())):
        if evt.unit.is_alive():
            hazard.on_unit_enter(evt.unit)


def register_level_rules(level):
    if getattr(level, "_ethereal_rules_registered", False):
        return
    level.event_manager.register_global_trigger(EventOnUnitAdded, on_unit_added)
    level.event_manager.register_global_trigger(EventOnMoved, on_unit_moved)
    level._ethereal_rules_registered = True


# Preserve the original initializer.
_original_level_init = Level.__init__


def level_init_with_ethereal_rules(self, w, h):
    # Initialize the level normally, including its event manager.
    _original_level_init(self, w, h)
    self.hazards = []
    register_level_rules(self)


def add_hazard(self, hazard, x, y):
    if not hasattr(self, "hazards"):
        self.hazards = []
    register_level_rules(self)

    hazard.x = x
    hazard.y = y
    hazard.level = self
    if not hasattr(hazard, "level_id"):
        hazard.level_id = self.level_id

    tile = self.tiles[x][y]
    if not hasattr(tile, "hazards"):
        tile.hazards = []
    if hazard not in tile.hazards:
        tile.hazards.append(hazard)
    if hazard not in self.hazards:
        self.hazards.append(hazard)
    return hazard


def remove_hazard(self, hazard):
    if hazard in self.hazards:
        self.hazards.remove(hazard)
    tile_hazards = getattr(self.tiles[hazard.x][hazard.y], "hazards", ())
    if hazard in tile_hazards:
        tile_hazards.remove(hazard)
    hazard.removed = True


# Replace the initializer.
Level.__init__ = level_init_with_ethereal_rules
Level.add_hazard = add_hazard
Level.remove_hazard = remove_hazard


def has_enemy_units_with_stasis(self):
    if any(u.team != TEAM_PLAYER for u in self.units):
        return True

    return any(
        getattr(hazard, "counts_for_level_clear", False)
        and getattr(hazard, "unit", None) is not None
        and hazard.unit.team != TEAM_PLAYER
        and hazard.unit.cur_hp > 0
        and not hazard.unit.killed
        for hazard in getattr(self, "hazards", ())
    )


Level.has_enemy_units = has_enemy_units_with_stasis


_original_rebuild_event_managers = Game.Game.rebuild_event_managers


def rebuild_event_managers_with_ethereal_rules(self):
    _original_rebuild_event_managers(self)

    levels = []
    seen = set()

    def add_level(level):
        if not level:
            return
        key = id(level)
        if key in seen:
            return
        seen.add(key)
        levels.append(level)
        for prop in getattr(level, "props", []):
            if not isinstance(prop, Portal):
                continue
            for next_level in (
                getattr(prop, "next_level", None),
                getattr(prop.level_gen_params, "level", None),
            ):
                if next_level:
                    add_level(next_level)

    add_level(self.cur_level)
    add_level(getattr(self, "next_level", None))
    add_level(getattr(self, "prev_next_level", None))

    for level in levels:
        level._ethereal_rules_registered = False
        if not hasattr(level, "hazards"):
            level.hazards = []
        for hazard in list(level.props):
            if not isinstance(hazard, EtherealHazard):
                continue
            level.props.remove(hazard)
            tile = level.tiles[hazard.x][hazard.y]
            if tile.prop is hazard:
                tile.prop = None
            add_hazard(level, hazard, hazard.x, hazard.y)
        register_level_rules(level)


Game.Game.rebuild_event_managers = rebuild_event_managers_with_ethereal_rules


PyGameView = sys.modules["__main__"].PyGameView
_original_try_examine_tile = PyGameView.try_examine_tile


def try_examine_tile_with_hazards(self, point):
    if point is None:
        return _original_try_examine_tile(self, point)

    level = self.get_display_level()
    if not level.is_point_in_bounds(point):
        return _original_try_examine_tile(self, point)

    tile = level.tiles[point.x][point.y]
    target = (tile.unit if tile.unit != self.game.p1 else None) or tile.cloud
    tile_hazards = getattr(tile, "hazards", ())
    if target is None and tile_hazards:
        target = tile_hazards[-1]
    if target is None:
        target = tile.prop
    self.examine_target = target


PyGameView.try_examine_tile = try_examine_tile_with_hazards

# original_get_sprite_sheet = PyGameView.get_sprite_sheet

# def get_sprite_sheet_debug(self, asset, radius=0):
#     print("DEBUG SpriteSheet asset:", repr(asset))
#     print("DEBUG SpriteSheet radius:", repr(radius))
#     return original_get_sprite_sheet(self, asset, radius)
        
# PyGameView.get_sprite_sheet = get_sprite_sheet_debug

original_on_damaged = SlimeAdaptiveArmorBuff.on_damaged

def on_damaged_patched(self, evt):
    if evt.damage <= 0:
        return

    form = self.dtypes_to_assets.get(evt.damage_type)

    # No sprite for this damage type: keep the current form.
    if form is None:
        if self.prev_res:
            self.owner.resists[self.prev_res] -= 100
        self.owner.resists[evt.damage_type] += 100
        self.prev_res = evt.damage_type
        return

    return original_on_damaged(self, evt)

SlimeAdaptiveArmorBuff.on_damaged = on_damaged_patched

reward_table = LevelRewards.reward_table

for i, reward in enumerate(reward_table):
    if reward[0] == LevelRewards.vault_portal_reward:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.vault_portal_reward, .02, 4, LevelRewards.vault_valid, "Vault Portal")
        continue
    if reward[0] == LevelRewards.reformation_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.reformation_shrine, .005, 4, None, "Shrine of Reformation")
        continue
    if reward[0] == LevelRewards.offering_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.offering_shrine, .005, None, LevelRewards.good_offering, "Shrine of Offering")
        continue
    if reward[0] == LevelRewards.rare_component_reward:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.rare_component_reward, .4, None, None, "Rare Component")
        continue
    if reward[0] == LevelRewards.knowledge_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.knowledge_shrine, .04, None, LevelRewards.spellslots_available, "Shrine of Knowledge")
        continue
    if reward[0] == LevelRewards.haste_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.haste_shrine, .03, None, None, "Shrine of Haste")
        continue
    if reward[0] == LevelRewards.chronomancy_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.chronomancy_shrine, .03, 5, None, "Chronomancy Shrine")
        continue
    if reward[0] == LevelRewards.duplication_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.duplication_shrine, .03, 5, None, "Duplication Shrine")
        continue
    if reward[0] == LevelRewards.perfection_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.perfection_shrine, .03, 8, None, "Shrine of Perfection")
        continue
    if reward[0] == LevelRewards.spellgraft_shrine:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.spellgraft_shrine, .03, 5, None, "Spellgraft Shrine")
        continue
    
    if reward[0] == LevelRewards.bookshelf:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.bookshelf, .04, None, None, "Bookshelf")
        continue
    if reward[0] == LevelRewards.scroll:
        # reward, weight, min_level, restrict fn, name
        reward_table[i] = (LevelRewards.scroll, .04, None, LevelRewards.spellslots_available, "Spell Scroll")
        continue

LevelRewards.reward_table = reward_table