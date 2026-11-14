import LevelRewards
import ModHandler
from Level import Color, EventOnUnitAdded, Level, Tag, Tags, Upgrade
# import sys
# PyGameView = sys.modules["__main__"].PyGameView

from RareMonsters import SlimeAdaptiveArmorBuff

#TODO staff with minion health / number
#TODO staff with damage, range and minion damage, range 4 3 4 3
#TODO repalce dummy goblins in hazards with unit free clartiy versions of the hazards 
#TODO unit previews !?
#TODO make euqipment staff that gives bonus charges and duration
#TODO make icons animated again!
#TODO fix level clear plus hazard remove chasms!?
#TODO ethermancer trial give ethermancer robe
#TODO make offmap spells use same helper for unit copy etc
#TODO fix description color and variables in spells/equipment
#TODO make spells/equipment scale with appropiate spell bonuses where not already done. Mostly missing for upgrades / equipment
#TODO Rename skill folder to equipment and make sure imports etc dont break 
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


# Preserve the original initializer.
_original_level_init = Level.__init__


def level_init_with_ethereal_rules(self, w, h):
    # Initialize the level normally, including its event manager.
    _original_level_init(self, w, h)

    # Register the rules for this level.
    self.event_manager.register_global_trigger(
        EventOnUnitAdded,
        on_unit_added
    )


# Replace the initializer.
Level.__init__ = level_init_with_ethereal_rules

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