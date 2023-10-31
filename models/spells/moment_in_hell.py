import copy
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.hell_stasis import HellStasis
from mods.EtherealPack.tags.Ethereal import Ethereal

class MomentInHell(Spell): # deal äthereal damage on cast? #Gives Clarity and cant target clarity

	def on_init(self):
		self.name = "A Moment in Hell"
		self.range = 7 
		self.tags = [Ethereal, Tags.Fire, Tags.Enchantment]
		self.level = 3

		self.duration = 3
		self.damage = 5
		self.damage_type = Ethereal

		self.max_charges = 4
		self.can_target_empty = False

		self.upgrades['max_charges'] = (3, 1)
		self.upgrades['damage'] = (9, 4)
		self.upgrades['duration'] = (4, 2)
		self.upgrades['brimstone'] = (1, 3, "Brimstone", "Deal [{damage}_fire:fire] and [{damage}_äthereal:äthereal] to 3 random enemies in a [5_tile:radius] radius around the target every turn")
		self.upgrades['explosive_entry'] = (1, 5, "Explosive Entry", "When the target reappiers or dies in the Fire Plane deal [fire:fire] and [äthereal:äthereal] damage equal to 1/4 of the targets missing hp to all units in a radius equal to 1/8 of the targets maximum hp until 32 hp then 1/16")

	def can_cast(self, x, y):
		unit = self.caster.level.get_unit_at(x,y)
		if unit and unit.has_buff(StunImmune):
			return False
		return super().can_cast(x, y)

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)

		unit_copy = copy.copy(unit)
		unit.kill(None, False) 
		for buff in unit.buffs:
			buff.apply(unit_copy)

		stasis = HellStasis(self.caster,self,self.get_stat('duration'),self.get_stat('damage'),unit_copy,self.get_stat('brimstone'),self.get_stat('explosive_entry'))
		self.caster.level.add_obj(stasis, unit.x, unit.y)

		yield

	def get_description(self):
		return "Transport target into the Plane of Fire for [{duration}_turns:duration]. Target suffers [{damage}_fire:fire] every turn until it reappiers.\nLeaves behind a Hell Portal that deals [{damage}_fire:fire] to enemies and applies Ätherealness for 2 turns.".format(**self.fmt_dict())