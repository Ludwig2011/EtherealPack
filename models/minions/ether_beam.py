
import random
from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherBeam(Spell):
	def __init__(self, elemental,damage):
		Spell.__init__(self)

		self.name = "Äther Beam"
		self.damage = damage
		self.beam = True
		self.cool_down = 7
		self.dtypes = [Ethereal]
		if elemental:
			self.dtypes.append(random.choice([Tags.Fire,Tags.Ice,Tags.Lightning]))

	def get_description(self):
		return "Shoots an Äther Beam"

	def cast(self, x, y):

		start = Point(self.caster.x, self.caster.y)
		target = Point(x, y)

		for point in Bolt(self.caster.level, start, target, find_clear=True):
			self.hit(point.x, point.y, self.dtypes)
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
		unit = self.caster.level.get_unit_at(x, y)
		if not unit or are_hostile(self.caster, unit):
			for dtype in dtypes:
				self.caster.level.deal_damage(x, y, self.get_stat('damage'), dtype, self)