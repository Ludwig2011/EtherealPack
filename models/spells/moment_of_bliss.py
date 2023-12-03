import copy
from Level import *
from mods.EtherealPack.models.hazards.bliss_stasis import BlissStasis
from mods.EtherealPack.tags.Ethereal import Ethereal

class MomentOfBliss(Spell):

	def on_init(self):
		self.name = "A Moment in Heaven"
		self.range = 7 
		self.tags = [Ethereal, Tags.Holy, Tags.Enchantment, Tags.Translocation]
		self.level = 2

		self.duration = 7
		self.damage = 3
		self.radius = 7

		self.max_charges = 4
		self.can_target_empty = False
		self.requires_los = False

		self.upgrades['max_charges'] = (3, 1)
		self.upgrades['range'] = (7, 2)
		self.upgrades['duration'] = (-4, 2)
		self.upgrades['blind'] = (1, 3, "Blinding Grace", "Blind enemies in [{radius}_radius:radius] for 3 turns every turn")
		self.upgrades['bless'] = (1, 5, "Blessing", "Yor ally gains 100 Holy resist, a ranged attack that deals [7_holy:holy] damage with 7 range and 3 HP regen")

	def can_cast(self, x, y):
		unit = self.caster.level.get_unit_at(x,y)
		if (unit and (unit.has_buff(StunImmune) or are_hostile(unit, self.caster))) or not self.caster.level.tiles[x][y].prop == None:
			return False
		return super().can_cast(x, y)

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)

		unit_copy = copy.copy(unit)
		unit.kill(None, False) 
		for buff in unit.buffs:
			buff.apply(unit_copy)

		stasis = BlissStasis(self.caster,self,self.get_stat('duration'),self.get_stat('radius'),self.get_stat('damage'),unit_copy,self.get_stat('blind'),self.get_stat('bless'))
		self.caster.level.add_obj(stasis, unit.x, unit.y)
			
		yield

	def get_description(self):
		return "Transport ally into the Plane of Bliss for [{duration}_turns:duration]. Ally restores [{damage}_hp:heal] every turn until they reappier.\nLeaves behind a blissfull Rift that heals allies [{damage}_hp:heal] hp in [{radius}_tile:range] range around the rift every turn and applies Ätherealness to units ontop for 2 turns.".format(**self.fmt_dict())
	