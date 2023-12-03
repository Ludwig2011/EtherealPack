from CommonContent import SimpleRangedAttack
from Level import *
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.models.hazards.util import add_unit, deal_damage


class Stasis(TileHazardBasic):
    def __init__(self, user, source, duration, unit, hazards=0, unit_buffs=None):
        TileHazardBasic.__init__(self, "Ether Portal", duration, user)
        self.source = source
        self.unit = unit
        self.unit_buffs = unit_buffs
        self.hazards = hazards
        self.asset = ["EtherealPack", "stasis"]
        self.gigantism = False
        self.player = [u for u in self.user.level.units if u.is_player_controlled][0]
        for skill in self.player.get_skills():
            if skill.name == "Äther Gigantism":
                self.gigantism = True

    def get_description(self):
        return ("%s in Stasis\n%d turns remaining\n"
                "Units standing on top get [Ätherealiesed:äthereal] for 2 turns" % (self.unit.name, self.duration))

    def effect(self, unit):
        pass

    def advance_effect(self):
        if self.gigantism and not are_hostile(self.unit, self.user):
            self.unit.max_hp += 5
            self.unit.cur_hp += 5
            for spell in self.unit.spells:
                if hasattr(spell, "damage"):
                    spell.damage += 2

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
        if self.unit.cur_hp <= 0:
            self.duration = 1
        if self.duration <= 1 and not self.unit.cur_hp <= 0:
            blocking_unit = self.user.level.get_unit_at(self.x,self.y)
            if not blocking_unit:
                add_unit(self.user.level,self.unit, self.x, self.y, self.unit_buffs)
                self.user.level.show_effect(self.x, self.y, Tags.Conjuration)
                if self.unit.gets_clarity:
                    self.unit.apply_buff(StunImmune(),2)
            else:
                p = self.user.level.get_summon_point(self.x, self.y, 20)
                if p:
                    add_unit(self.user.level,self.unit, p.x, p.y, self.unit_buffs)
                    self.user.level.show_effect(p.x, p.y, Tags.Conjuration)
                    if self.unit.gets_clarity:
                        self.unit.apply_buff(StunImmune(),2)