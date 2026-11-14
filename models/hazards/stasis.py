from Level import *
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.models.hazards.util import (
    add_unit,
    suspend_unit_events,
)


class TranslocationStasis(TileHazardBasic):
    def __init__(self, name, asset, user, source, duration, unit, unit_buffs=None):
        TileHazardBasic.__init__(self, name, duration, user)
        self.source = source
        self.unit = unit
        if unit is not None:
            suspend_unit_events(unit)
        self.unit_buffs = unit_buffs
        self.asset = asset
        self.player = next(u for u in self.user.level.units if u.is_player_controlled)
        self.gigantism = any(
            item.name == "Äther Gigantism" for item in self.player.get_equipment()
        )

    def apply_gigantism(self):
        if self.unit is not None and self.gigantism and not are_hostile(
            self.unit, self.user
        ):
            self.unit.max_hp += 5
            self.unit.cur_hp += 5
            for spell in self.unit.spells:
                if hasattr(spell, "damage"):
                    spell.damage += 2

    def effect(self, unit):
        pass

    def on_unit_returned(self):
        pass

    def return_unit(self):
        if self.unit is None or self.duration > 1 or self.unit.cur_hp <= 0:
            return

        level = self.user.level
        if not level.get_unit_at(self.x, self.y):
            point = Point(self.x, self.y)
        else:
            point = level.get_summon_point(self.x, self.y, 20)
        if not point:
            return

        add_unit(level, self.unit, point.x, point.y, self.unit_buffs)
        self.on_unit_returned()
        level.show_effect(point.x, point.y, Tags.Conjuration)
        if self.unit.gets_clarity:
            self.unit.apply_buff(StunImmune(), 2)


class Stasis(TranslocationStasis):
    def __init__(self, user, source, duration, unit, hazards=0, unit_buffs=None):
        TranslocationStasis.__init__(
            self,
            "Ether Portal",
            ["EtherealPack", "stasis"],
            user,
            source,
            duration,
            unit,
            unit_buffs,
        )
        self.hazards = hazards

    def get_description(self):
        unit_name = self.unit.name if self.unit is not None else "Empty Ether Portal"
        return ("%s in Stasis\n%d turns remaining\n"
                "Units standing on top get [Ätherealiesed:äthereal] for 2 turns" % (unit_name, self.duration))

    def advance_effect(self):
        self.apply_gigantism()

        steppy = self.user.level.get_unit_at(self.x,self.y)
        if steppy: 
            steppy.apply_buff(EtherealnessBuff(), 2)
        tiles = [t for t in self.user.level.get_points_in_ball(self.x,self.y,5) if self.user.level.tiles[t.x][t.y].prop == None and self.user.level.tiles[t.x][t.y].can_see]
        if len(tiles)>0:
            for i in range(self.hazards):
                if len(tiles)<=0:
                    continue
                tile = random.choice(tiles)
                self.user.level.add_obj(PureEther(self.user,self.source,3,7, self.user.level.tiles[tile.x][tile.y].is_chasm), tile.x, tile.y)
                tiles.remove(tile)
        if self.unit is not None and self.unit.cur_hp <= 0:
            self.duration = 1
        self.return_unit()