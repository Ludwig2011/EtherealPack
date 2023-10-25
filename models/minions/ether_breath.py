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
		if self.elemental:
			dtypes1 = [Ethereal,Tags.Fire]
			dtypes2 = [Ethereal,Tags.Lightning]
			dtypes3 = [Ethereal,Tags.Ice]
		else:
			dtypes1 = [Ethereal]
			dtypes2 = [Ethereal]
			dtypes3 = [Ethereal]
		start = Point(self.caster.x, self.caster.y)
		target = Point(x, y)

		for point in Bolt(self.caster.level, start, target, find_clear=True):
			self.hit(point.x, point.y, dtypes1)

		target = self.get_ai_target()
		if target:
			for point in Bolt(self.caster.level, start, target, find_clear=True):
				self.hit(point.x, point.y, dtypes2)

		target = self.get_ai_target()
		if target:
			for point in Bolt(self.caster.level, start, target, find_clear=True):
				self.hit(point.x, point.y, dtypes3)
		yield

	def get_impacted_tiles(self, x, y):
		tiles = set()
		tiles.add(Point(x, y))

		target = Point(x, y)

		if self.beam:
			for p in Bolt(self.caster.level, self.caster, target):
				tiles.add(p)

		return tiles				

	def hit(self, x, y, dtypes):
		unit = self.caster.get_unit_at(x, y)
		if not unit or are_hostile(self.caster, unit):
			for dtype in dtypes:
				self.caster.deal_damage(x, y, self.get_stat('damage'), dtype, self)