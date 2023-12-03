	
from Level import Tags, are_hostile
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff


class Brimstone(TileHazardBasic):
    def __init__(self, user, source, duration, damage, ether=False):
        if ether:
            TileHazardBasic.__init__(self, "Hell Portal", duration, user)
            self.asset = ["EtherealPack", "Hell_Stasis"]
        else:
            TileHazardBasic.__init__(self, "Brimstone", duration, user)
            self.asset = ["EtherealPack", "brimstone"]
        self.damage = damage
        self.ether = ether
        self.source = source

    def get_description(self):
        if self.ether:
            return "Units hostile to %s take %d [fire:fire] damage at the end of a turn, applies 2 turns of [Ätherealness:äthereal]\n%d turns remaining" % (self.user.name, self.damage, self.duration) 
        else:
            return "Units hostile to %s take %d [fire:fire] damage at the end of a turn\n%d turns remaining" % (self.user.name, self.damage, self.duration)

    def effect(self, unit):
        pass

    def advance_effect(self):
        unit = self.user.level.get_unit_at(self.x, self.y)
        if unit is not None:
            if self.ether:
                unit.apply_buff(EtherealnessBuff(),2)
            if are_hostile(self.user, unit):
                self.user.level.deal_damage(self.x, self.y, self.damage, Tags.Fire, self.source)