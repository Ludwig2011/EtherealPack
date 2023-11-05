from Level import *
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.tags.Ethereal import Ethereal


class DomainExpansionSpell(Spell):

    def on_init(self):

        self.name = "Domain Expansion"
        
        self.level = 1
        self.max_charges = 0

        self.damage = 7
        self.radius = 5
        self.duration = 4

        self.stun = False
        self.shields = 0

        self.range = 1


            
        self.upgrades['stun'] = (True, 25)
        self.upgrades['damage'] = (1, 25)
        self.upgrades['radius'] = (1, 25)
        self.upgrades['shields'] = (1, 25)

        self.tags = [Tags.Sorcery, Tags.Chaos, Tags.Lightning, Ethereal]



    def get_description(self):
        return ("Ooooh much fluff, such storytelling")

    def cast_instant(self, x, y):
        hostile_targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u != self.caster and are_hostile(self.caster, u)]
        friendly_targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u != self.caster and not are_hostile(self.caster, u)]
        if self.get_stat("stun"):
            for target in hostile_targets:
                target.apply_buff(Stun(), 1)
        
        if self.get_stat("shields"):
            for target in friendly_targets:
                if target.shields < 2:
                    target.shields += 1                
                

        for stage in Burst(self.caster.level, self.caster.x, self.caster.y, self.get_stat('radius')):
            for point in stage:
                if self.caster.level.tiles[point.x][point.y].prop == None:
                    pure_ether = PureEther(self.caster,self,self.get_stat('duration'),self.get_stat('damage'))
                    self.caster.level.add_obj(pure_ether, point.x, point.y)
