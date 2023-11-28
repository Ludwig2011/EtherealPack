from CommonContent import FrozenBuff
from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
import random


class EtherStormSpell(Spell):

    def on_init(self):

        self.name = "Äther Storm"
        self.level = 2
        self.asset = ['EtherealPack', 'ether_storm']

        self.amount_of_strikes = 7
        self.range = 11
        self.max_charges = 10
        self.damage = 7
        self.radius = 5
        self.chance = 25
        self.duration = 7
        self.requires_los = True

              
        self.upgrades['chance'] = (25, 1)      
        self.upgrades['amount_of_strikes'] = (7, 2)
        self.upgrades['max_charges'] = (11, 3)
        self.upgrades['requires_los'] = (-1, 2, "Blindcasting", "Äther Storm can be cast without line of sight")  
        self.upgrades['endothermic_discharge'] = (1, 1, "Endothermic Discharge", "The bolts have a %d percent chance to freeze enemies for 1 turns" % (self.get_stat('chance')/2))
        self.upgrades['lingering_static'] = (1, 2, "Lingering Static", "The Storms static field applies Ätherealness to all units for [{duration}_turns:duration]")
        self.upgrades['searing_storm'] = (1, 3, "Searing Storm", "The bolts have a %d percent chance to leave enemies with burns dealing [{damage}_fire:fire] damage for 3 turns" % (self.get_stat('chance')/2))

        self.tags = [Tags.Sorcery, Tags.Chaos, Tags.Lightning, Ethereal]



    def get_description(self):
        return ("Open a Rift to the Energy Plane through which %d energy bolts strike random enemies in [{radius}_radius:radius]\n"
                "Each bolt deals [{damage}_äthereal:äthereal] damage and has a %d percent chance to deal lightning damage aswell\n"
                "The Chance of added effects from this spell is doubled against [ätherealiesed:äthereal] targets" % (self.get_stat('amount_of_strikes'), self.get_stat('chance'))).format(**self.fmt_dict())

    def cast(self, x, y):
        targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u != self.caster and are_hostile(self.caster, u)]
        
        for i in range(self.get_stat('amount_of_strikes')):
            if len(targets) < 1:
                continue
            target = random.choice(targets)
            chance = self.get_stat('chance')*2 if target.has_buff(EtherealnessBuff) else self.get_stat('chance')
            if self.get_stat('endothermic_discharge') and random.random()*100 < chance/2:
                target.apply_buff(FrozenBuff(), 1)
            if self.get_stat('searing_storm') and random.random()*100 < chance/2:
                target.apply_buff(EtherBuff(self.get_stat('damage')), 3) 
            if random.random()*100 < chance:
                self.caster.level.deal_damage(target.x, target.y, self.damage, Tags.Lightning, self) 
            self.caster.level.deal_damage(target.x, target.y, self.damage, Ethereal, self)
            if target.cur_hp < 1:
                targets.remove(target)

        targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u.cur_hp > 0]
        if self.get_stat('lingering_static'):
            for target in targets:
                target.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
        yield

class EtherBuff(Buff):

	def __init__(self, damage):
		self.damage = damage
		Buff.__init__(self)

	def on_init(self):
		self.name = "Burning (%d)" % self.damage
		self.description = "At end of this units turn, it takes %d damage." % self.damage
		self.asset = ['status', 'burning']

	def on_advance(self):
		self.owner.deal_damage(self.damage, Tags.Fire, self)