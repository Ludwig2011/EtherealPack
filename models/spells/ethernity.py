import copy
from Level import *
from Monsters import Goblin
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.brimstone import Brimstone
from mods.EtherealPack.models.hazards.hell_stasis import HellStasis
from mods.EtherealPack.models.hazards.stasis import Stasis
from mods.EtherealPack.models.hazards.util import get_hazard_point
from mods.EtherealPack.tags.Ethereal import Ethereal

class Ethernity(Spell): # mordred???????????????????????????????

	def on_init(self):
		self.name = "Äthernity"
		self.range = 7 
		self.tags = [Ethereal, Tags.Enchantment, Tags.Translocation]
		self.level = 2

		self.duration = 7
		self.damage = 5
		self.damage_type = Ethereal

		self.max_charges = 11
		self.can_target_empty = False

		self.upgrades['max_charges'] = (10, 2)
		self.upgrades['duration'] = (7, 2)
		self.upgrades['range'] = (7, 2)
		self.upgrades['hazards'] = (1, 2, "Pertrusion", "Leave behind 3 pure ether hazards for 3 turns that deal [7_äthereal:äthereal] damage in a 5 tile radius around the rift")

	def can_cast(self, x, y):
		unit = self.caster.level.get_unit_at(x,y)
		if (unit and unit.has_buff(StunImmune)) or get_hazard_point(self.caster.level,x,y,flying=unit.flying)==None:
			return False
		return super().can_cast(x, y)

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		hazard_point = get_hazard_point(self.caster.level,x,y,flying=unit.flying)
		hazards = 3 if self.get_stat('hazards') else 0

		if not unit.gets_clarity:
			unit_copy = copy.copy(unit)
			unit.kill(None, False) 
			for buff in unit.buffs:
				buff.apply(unit_copy)
			stasis = Stasis(self.caster,self,self.get_stat('duration'),unit_copy,hazards)
			self.caster.level.add_obj(stasis, hazard_point.x, hazard_point.y)
		else:
			unit.apply_buff(Stun(), self.get_stat('duration'))
			stasis = Stasis(self.caster,self,self.get_stat('duration'),Goblin(),hazards)
			self.caster.level.add_obj(stasis, hazard_point.x, hazard_point.y)

		yield

	def get_description(self):
		return "Transport target into the Ether Plane for [{duration}_turns:duration].\nLeaves behind a Rift that [ätherealieses:äthereal] units for 2 turns.".format(**self.fmt_dict())
