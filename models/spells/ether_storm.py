from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
import random


class EtherStormSpell(Spell):

    def on_init(self):

        self.name = "Ether Storm"
        self.level = 1

        self.range = 4
        self.charges = 8
        self.amount_of_strikes = 3
        self.damage = 11
        self.duration = 7

        self.radius = 4
            
        self.upgrades['amount_of_strikes'] = (2, 2)
        self.upgrades['range'] = (2, 3)
        self.upgrades['charges'] = (1, 4)
        self.upgrades['damage'] = (1, 5)        
        self.upgrades['lingering_static'] = (1, 4)
        self.upgrades['searing_storm'] = (1, 3)

        self.tags = [Tags.Dragon, Tags.Conjuration, Ethereal]



    def get_description(self):
        return ("1337")

    def cast(self, x, y):
        targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u != self.caster and are_hostile(self.caster, u)]
        
        if self.get_stat("lingering_static"):
            for target in targets:
                target.apply_buff(EtherealnessBuff(), self.get_stat("duration"))

        
        for x in range(self.amount_of_strikes):
            if len(targets) < 1:
                continue
            target = random.choice(targets)
            if self.get_stat("searing_storm"):
                self.caster.level.deal_damage(target.x, target.y, self.damage, Ethereal, self) # Change later --> see ETH-24
            self.caster.level.deal_damage(target.x, target.y, self.damage, Ethereal, self)
            if target.cur_hp < 1:
                targets.remove(target)
        yield
