import copy
from Level import *
from Monsters import Goblin
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.brimstone import Brimstone
from mods.EtherealPack.models.hazards.hell_stasis import HellStasis
from mods.EtherealPack.models.hazards.util import get_hazard_point
from mods.EtherealPack.tags.Ethereal import Ethereal

class MomentInHell(Spell): # mordred???????????????????????????????

	def on_init(self):
		self.name = "A Moment in Hell"
		self.range = 7 
		self.tags = [Ethereal, Tags.Fire, Tags.Enchantment, Tags.Translocation]
		self.level = 3

		self.duration = 3
		self.damage = 5
		self.damage_type = Ethereal

		self.max_charges = 4
		self.can_target_empty = False

		self.upgrades['max_charges'] = (3, 1)
		self.upgrades['damage'] = (9, 4)
		self.upgrades['duration'] = (4, 2)
		self.upgrades['brimstone'] = (1, 3, "Brimstone", "Fragments leave behind brimstone hazards for 3 turns that deal [fire:fire] damage")
		self.upgrades['explosive_entry'] = (1, 5, "Explosive Entry", "When the target reappiers or dies in the Fire Plane deal [fire:fire] and [äthereal:äthereal] damage equal to 1/4 of the targets missing hp to all units in a radius equal to 1/8 of the targets maximum hp until 32 hp then 1/16")

	def can_cast(self, x, y):
		unit = self.caster.level.get_unit_at(x,y)
		if unit and (unit.has_buff(StunImmune) or unit.has_buff(StunImmune) or get_hazard_point(self.caster.level,x,y,flying=unit.flying)==None):
			return False
		return super().can_cast(x, y)

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		hazard_point = get_hazard_point(self.caster.level,x,y,flying=unit.flying)
		if not unit.gets_clarity:
			unit_copy = copy.copy(unit)
			unit.kill(None, False) 
			for buff in unit.buffs:
				buff.apply(unit_copy)

			stasis = HellStasis(self.caster,self,self.get_stat('duration'),self.get_stat('damage'),unit_copy,self.get_stat('brimstone'),self.get_stat('explosive_entry'))
			self.caster.level.add_obj(stasis, hazard_point.x, hazard_point.y)
		else:
			unit.apply_buff(Stun(), self.get_stat('duration'))
			stasis = HellStasis(self.caster,self,self.get_stat('duration'),self.get_stat('damage'),Goblin(),self.get_stat('brimstone'),self.get_stat('explosive_entry'))
			self.caster.level.add_obj(stasis, hazard_point.x, hazard_point.y)

		yield

	def get_description(self):
		return "Transport target into the Plane of Fire for [{duration}_turns:duration]. Target suffers [{damage}_fire:fire] every turn until it reappiers.\nLeaves behind a Hell Rift that deals [{damage}_fire:fire] to enemies and applies [Ätherealness:äthereal] for 2 turns\n Every turn fragments deal [{damage}_fire:fire] and [{damage}_äthereal:äthereal] to 3 random enemies in a [5_tile:radius] radius around the rift.".format(**self.fmt_dict())
