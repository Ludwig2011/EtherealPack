import copy
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.hell_stasis import HellStasis
from mods.EtherealPack.tags.Ethereal import Ethereal

class MomentOfBliss(Spell): # mordred???????????????????????????????

	def on_init(self):
		self.name = "A Moment of Bliss"
		self.range = 7 
		self.tags = [Ethereal, Tags.Holy, Tags.Enchantment]
		self.level = 3

		self.duration = 3
		self.damage = 3

		self.max_charges = 4
		self.can_target_empty = False

		self.upgrades['max_charges'] = (3, 1)
		self.upgrades['duration'] = (4, 3)
		self.upgrades['stunning_entry'] = (1, 3, "Stunning Entry", "When the target reappiers stun all units in a [{radius}_radius:radius] for 2 turns")
		self.upgrades['sunlight'] = (1, 4, "Sunlight", "Provide healing and shielding in a [{radius}_radius:radius] aswell")
		self.upgrades['blessing'] = (1, 5, "Blessing", "The target gains power every turn ")

	def can_cast(self, x, y):
		unit = self.caster.level.get_unit_at(x,y)
		if (unit and unit.has_buff(StunImmune)) or not self.caster.level.tiles[x][y].prop == None:
			return False
		return super().can_cast(x, y)

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)

		if not unit.gets_clarity:
			unit_copy = copy.copy(unit)
			unit.kill(None, False) 
			for buff in unit.buffs:
				buff.apply(unit_copy)

			stasis = HellStasis(self.caster,self,self.get_stat('duration'),self.get_stat('damage'),unit_copy,self.get_stat('brimstone'),self.get_stat('explosive_entry'))
			self.caster.level.add_obj(stasis, unit.x, unit.y)
		else:
			unit.apply_buff(Stun(), self.get_stat('duration'))
			stasis = Brimstone(self.caster,self,self.get_stat('duration'),self.get_stat('damage'))
			self.caster.level.add_obj(stasis, unit.x, unit.y)
			
		yield

	def get_description(self):
		return "Transport target into the Plane of Bliss for [{duration}_turns:duration]. Target restors [{damage}_hp:heal] every turn until it reappiers.\nLeaves behind a blissfull Portal that heals [{damage}_hp:heal] to allies and applies Ätherealness for 2 turns.".format(**self.fmt_dict())
	