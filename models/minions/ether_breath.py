import random

from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal
#spell hex debuff target takes extra dmg from all sources/skillsandspells

class EtherBreath(Spell):
	def __init__(self, elemental):
		Spell.__init__(self)

		self.name = "Äther Breath"
		self.damage = 7
		self.beam = True
		self.cool_down = 7
		self.elemental = elemental

	def get_description(self):
		return "Breaths out three Äther Beams"

	def cast(self, x, y):
		start = Point(self.caster.x, self.caster.y)
		target = Point(x, y)

		for point in Bolt(self.caster.level, start, target, find_clear=True):
			self.hit(point.x, point.y)

		target = self.get_ai_target()
		if target:
			for point in Bolt(self.caster.level, start, target, find_clear=True):
				self.hit(point.x, point.y)

		target = self.get_ai_target()
		if target:
			for point in Bolt(self.caster.level, start, target, find_clear=True):
				self.hit(point.x, point.y)
		yield

	def get_impacted_tiles(self, x, y):
		tiles = set()
		tiles.add(Point(x, y))

		target = Point(x, y)

		if self.beam:
			for p in Bolt(self.caster.level, self.caster, target):
				tiles.add(p)

		return tiles				

	def hit(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		if not unit:
			self.caster.level.deal_damage(x, y, self.get_stat('damage'), Ethereal, self)
		elif are_hostile(self.caster, unit):
			self.caster.level.deal_damage(x, y, self.get_stat('damage'), Ethereal, self)
			if self.elemental:
				elements = [Tags.Fire, Tags.Lightning, Tags.Ice]
				weakest_resist = min(unit.resists[element] for element in elements)
				weakest_elements = [element for element in elements if unit.resists[element] == weakest_resist]
				self.caster.level.deal_damage(x, y, self.get_stat('damage'), random.choice(weakest_elements), self)