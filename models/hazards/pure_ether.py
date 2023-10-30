from Level import *
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class PureEther(TileHazardBasic):
    def __init__(self, user, source, duration, damage):
        TileHazardBasic.__init__(self, "Pure Ether", duration, user)
        self.damage = damage
        self.source = source
       # self.asset = ["Plague", "blood_puddle"]

    def get_description(self):
        return "Units hostile to %s take %d [äthereal:äthereal] damage at the end of a turn, applies 2 turns of [Ätherealness:äthereal]\n%d turns remaining" % (self.user.name, self.damage, self.duration) 

    def effect(self, unit):
        pass

    def advance_effect(self):
        unit = self.user.level.get_unit_at(self.x, self.y)
        unit.apply_buff(EtherealnessBuff(),2)
        if unit is not None and are_hostile(self.user, unit):
            self.user.level.deal_damage(self.x, self.y, self.damage, Ethereal, self.source)