from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal


class ExpandingForceBuff(Buff):

	def __init__(self, damage, damage_type, radius, friendly_fire=False, melt_walls=False):
			Buff.__init__(self)
			self.damage = damage
			self.damage_type = damage_type
			self.radius = radius
			self.friendly_fire = friendly_fire
			self.source = None
			if isinstance(self.damage_type, Tag):
				self.name = "%s Aura" % self.damage_type.name
			else:
				self.name = "Damage Aura" 


			self.melt_walls = melt_walls

	def on_advance(self):

		effects_left = 7

		for unit in self.owner.level.get_units_in_ball(Point(self.owner.x, self.owner.y), self.radius):
			if unit == self.owner:
				continue

			if not self.friendly_fire and not self.owner.level.are_hostile(self.owner, unit):
				continue

			if isinstance(self.damage_type, list):
				damage_type = random.choice(self.damage_type)
			else:
				damage_type = self.damage_type
			unit.deal_damage(self.damage, damage_type, self.source or self)
			# move unit
			self.push(unit,self.owner,1)
			effects_left -= 1

		# Show some graphical indication of this aura if it didnt hit much
		points = self.owner.level.get_points_in_ball(self.owner.x, self.owner.y, self.radius)
		points = [p for p in points if not self.owner.level.get_unit_at(p.x, p.y)]
		random.shuffle(points)
		for i in range(effects_left):
			if not points:
				break
			p = points.pop()
			if isinstance(self.damage_type, list):
				damage_type = random.choice(self.damage_type)
			else:
				damage_type = self.damage_type
			self.owner.level.deal_damage(p.x, p.y, 0, damage_type, source=self.source or self)

			# Wall melting
			if self.melt_walls and not self.owner.level.tiles[p.x][p.y].can_see:
				self.owner.level.make_floor(p.x, p.y)

	def push(target, source, squares):
		direction_x = source.x - target.x
		direction_y = source.y - target.y

		# Make sure to check if the direction is non-zero to avoid division by zero
		if direction_x != 0:
			opposite_x = target.x + squares * (direction_x // abs(direction_x))
		else:
			opposite_x = target.x

		if direction_y != 0:
			opposite_y = target.y + squares * (direction_y // abs(direction_y))
		else:
			opposite_y = target.y

		if target.level.can_move(target, opposite_x, opposite_y, teleport=True):
			target.level.act_move(target, opposite_x, opposite_y, teleport=True)
			return True
		else:
			return False


	def can_threaten(self, x, y):
		return distance(self.owner, Point(x, y)) <= self.radius

	def get_tooltip(self):
		damage_type_str = ' or '.join(t.name for t in self.damage_type) if isinstance(self.damage_type, list) else self.damage_type.name
		unit_type_str = 'units' if self.friendly_fire else 'enemy units'
		return "Each turn, deals %d %s damage to %s in a %d tile radius and pushes enemies back 1 tile" % (self.damage, damage_type_str, unit_type_str, self.radius)



class ExpandingForceSpell(Spell):

	def on_init(self):

		self.range = 0
		self.max_charges = 3
		self.name = "Expanding Force"
		self.aura_damage = 2
		self.radius = 5
		self.duration = 7

		self.stats.append('aura_damage')

		self.upgrades['radius'] = (2, 1)
		self.upgrades['duration'] = (7, 2)

		self.upgrades['teleport_blocker'] = (1, 3, "Teleport Blocker", "When an enemy teleports inside this .")
		
		self.tags = [Tags.Enchantment, Ethereal, Tags.Arcane]
		self.level = 4

	def cast_instant(self, x, y):
		buff = ExpandingForceBuff(self, damage=self.spell.aura_damage, radius=self.spell.get_stat('radius'), damage_type=[Ethereal], friendly_fire=False)
		buff.stack_type = STACK_REPLACE
		buff.color = Ethereal.color
		buff.name = "Expanding Force Aura"
		buff.source = self
		self.caster.apply_buff(buff, self.get_stat('duration'))

	def get_description(self):
		return ("Each turn, deals [{aura_damage}_äthereal:äthereal] damage to each enemy and push them [1_tile:radius] away from the caster in a [{radius}_tile:radius] radius.\n"
				"This damage is fixed, and cannot be increased using shrines, skills, or buffs.\n"
				"Lasts [{duration}_turns:duration].").format(**self.fmt_dict())