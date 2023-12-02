import copy
from Level import *
from Monsters import Goblin
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.brimstone import Brimstone
from mods.EtherealPack.models.hazards.hell_stasis import HellStasis
from mods.EtherealPack.models.hazards.stasis import Stasis
from mods.EtherealPack.tags.Ethereal import Ethereal

class MassStasis(Spell): # mordred???????????????????????????????

    def on_init(self):
        self.name = "Mass Stasis"
        self.range = 7 
        self.tags = [Ethereal, Tags.Enchantment]
        self.level = 3

        self.duration = 4
        self.damage_type = Ethereal

        self.max_charges = 4
        self.can_target_empty = False

        self.upgrades['max_charges'] = (3, 1)
        self.upgrades['duration'] = (3, 1)
        self.upgrades['radius'] = (3, 1)
        self.upgrades['hazards'] = (3, 2, "Pertrusion", "Leave behind 3 pure ether hazards for 3 turns that deal [7_äthereal:äthereal] damage in a 5 tile radius around the rift")

    def can_cast(self, x, y):
        unit = self.caster.level.get_unit_at(x,y)
        if (unit and unit.has_buff(StunImmune)) or not self.caster.level.tiles[x][y].prop == None:
            return False
        return super().can_cast(x, y)

    def cast(self, x, y):
        for tile in self.caster.level.get_points_in_ball(x,y,self.get_stat('radius')):
            unit = self.caster.level.get_unit_at(tile.x, tile.y)

            if not unit.gets_clarity:
                unit_copy = copy.copy(unit)
                unit.kill(None, False) 
                for buff in unit.buffs:
                    buff.apply(unit_copy)

                stasis = Stasis(self.caster,self,self.get_stat('duration'),unit_copy)
                self.caster.level.add_obj(stasis, unit.x, unit.y)
            else:
                unit.apply_buff(Stun(), self.get_stat('duration'))
                stasis = Stasis(self.caster,self,self.get_stat('duration'),Goblin())
                self.caster.level.add_obj(stasis, unit.x, unit.y)

            yield

    def get_description(self):
        return "Transport target into the Ether Plane for [{duration}_turns:duration].\nLeaves behind a Rift that [ätherealieses:äthereal] units for 2 turns.".format(**self.fmt_dict())
