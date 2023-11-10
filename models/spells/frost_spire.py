from CommonContent import FrozenBuff, SimpleRangedAttack, pull
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class SummonFrostSpire(Spell):

	def on_init(self):
		self.name = "Frost Spire"
		self.range = 6
		self.max_charges = 4
		self.tags = [Tags.Enchantment, Ethereal, Tags.Conjuration, Tags.Ice]
		self.level = 4

		self.minion_health = 40
		self.minion_damage = 4
		self.radius = 4
		self.duration = 3
		self.upgrades['minion_health'] = (30, 2)
		self.upgrades['minion_damage'] = (3, 1)
		self.upgrades['range'] = (4, 2)
		self.upgrades['radius'] = (3, 3)
		self.upgrades['faulty_rift'] = (1, 2, "Faulty Rift", "The rift applies [Ätherealness:äthereal] to all units in [{radius}_radius:radius] for 7 turns")
		self.upgrades['implosive_entry'] = (1, 4, "Implosive Entry", "The rift pulls on all units in [{radius}_radius:radius] + 1 and deals 1/14 of its hp as [ice:ice] and [äthereal:äthereal] damage")
		self.upgrades['frost_mortem'] = (1, 6, "Frost Mortem", "Units that die within the Frost Aura of the Spire leave behind frost Golems\n"
		"Frost Golems have half the units hp, 1 shield and a melee attack that deals 4 [ice:ice] and 3 [physical:physical] damage\n"
		"Frost Golems have [75_ice:ice], [100_poison:poison], [25_physical:physical], [-25_fire:fire] resistance")
		self.must_target_empty = True

	def cast(self, x, y):		
		spire = FrostSpire(self.get_stat('minion_health'),self.get_stat('minion_damage'), self.get_stat('radius'))
		spire.team = self.caster.team
		spire.buffs.append(FrostAuraBuff(self.get_stat('radius'),self.get_stat('frost_mortem')))
		self.summon(spire, Point(x, y))
		
		if self.get_stat('implosive_entry'):
			for p in self.caster.level.get_points_in_ball(x, y, self.get_stat('radius')+1):
				unit = self.caster.level.get_unit_at(p.x, p.y)
				if unit:
					pull(unit, spire, 1)

		for p in self.caster.level.get_points_in_ball(x, y, self.get_stat('radius')):
			unit = self.caster.level.get_unit_at(p.x, p.y)
			if unit:
				if self.get_stat('implosive_entry') and not (p.x == x and p.y == y):
					self.caster.level.deal_damage(p.x, p.y, self.get_stat('minion_health')/14, Tags.Ice, self)
					self.caster.level.deal_damage(p.x, p.y, self.get_stat('minion_health')/14, Ethereal, self)
				if unit.cur_hp > 0:
					unit.apply_buff(FrozenBuff(), self.get_stat('duration'))
				if unit.cur_hp > 0 and self.get_stat('faulty_rift'):
					unit.apply_buff(EtherealnessBuff(), 7)
					self.caster.level.show_effect(p.x,p.y, Ethereal)


		yield

	def get_description(self):
		return ("Open a Rift to the Ice Plane that freezes all units in [{radius}_radius:radius] around the Rift for [{duration}:duration] turns and leave behind a stationary Frost Spire.\n"
				"Frost Spire has [{minion_health}_HP:minion_health] and [100_ice:ice], [100_poison:poison], [25_physical:physical], [-50_fire:fire] resistance.\n"
				"Frost Spire has a Forst Bolt attack which deals [{minion_damage}_ice:ice] damage and [freezes:ice] the target for 3 turns with [{radius}_range:range].\n"
				"Frost Spire has a Forst Aura which deals [3_ice:ice] damage to all units in [{radius}_radius:radius] around the Spire every turn.").format(**self.fmt_dict())

def FrostSpire(health,damage,range):
	unit = Unit()
	unit.sprite.char = 'D'
	unit.sprite.color = Color(1,121,111)
	unit.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
	unit.name = "Frost Spire"
	unit.stationary = True
	unit.description = "Fires Frost Bolts that freeze enemies"
	unit.max_hp = health
	unit.spells.append(SimpleRangedAttack("Frost Bolt", damage, Tags.Ice, range, cool_down=3, buff=FrozenBuff, buff_duration=3))
	unit.tags = [Tags.Ice, Tags.Construct]
	unit.resists[Tags.Ice] = 100
	unit.resists[Tags.Poison] = 100
	unit.resists[Tags.Physical] = 25
	unit.resists[Tags.Fire] = -50
	return unit

class FrostAuraBuff(Buff):

	def __init__(self, radius, frost_mortem):
		Buff.__init__(self)
		self.damage = 3
		self.damage_type = Tags.Ice
		self.radius = radius
		self.friendly_fire = False
		self.source = None
		self.frost_mortem = frost_mortem
		self.global_triggers[EventOnDeath] = self.on_death
		if isinstance(self.damage_type, Tag):
			self.name = "%s Aura" % self.damage_type.name
		else:
			self.name = "Damage Aura" 

	def on_advance(self):

		effects_left = 7
		for unit in self.owner.level.get_units_in_ball(Point(self.owner.x, self.owner.y), self.radius):
			if unit == self.owner:
				continue

			if not self.friendly_fire and not self.owner.level.are_hostile(self.owner, unit):
				continue

			unit.deal_damage(self.damage, self.damage_type, self.source or self)
			effects_left -= 1

		# Show some graphical indication of this aura if it didnt hit much
		points = self.owner.level.get_points_in_ball(self.owner.x, self.owner.y, self.radius)
		points = [p for p in points if not self.owner.level.get_unit_at(p.x, p.y)]
		random.shuffle(points)
		for i in range(effects_left):
			if not points:
				break
			p = points.pop()
			self.owner.level.deal_damage(p.x, p.y, 0, self.damage_type, source=self.source or self)

	def on_death(self, evt):
		if self.frost_mortem:
			points = []
			for p in self.owner.level.get_points_in_ball(self.owner.x, self.owner.y, self.radius):
				points.append(Point(p.x, p.y))
			if Point(evt.unit.x, evt.unit.y) in points:
				frost_golem = FrostGolem(math.ceil(evt.unit.max_hp/2))
				frost_golem.team = self.owner.team
				self.summon(frost_golem, Point(evt.unit.x, evt.unit.y))

	def can_threaten(self, x, y):
		return distance(self.owner, Point(x, y)) <= self.radius

	def get_tooltip(self):
		damage_type_str = ' or '.join(t.name for t in self.damage_type) if isinstance(self.damage_type, list) else self.damage_type.name
		unit_type_str = 'units' if self.friendly_fire else 'enemy units'
		return "Each turn, deals %d %s damage to %s in a %d tile radius" % (self.damage, damage_type_str, unit_type_str, self.radius)
	
def FrostGolem(health):
	unit = Unit()
	unit.sprite.char = 'D'
	unit.sprite.color = Color(1,121,111)
	unit.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
	unit.name = "Frost Golem"
	unit.description = "Punches Things, is cold"
	unit.shields = 1
	unit.max_hp = health
	unit.spells.append(FrostPunch())
	unit.tags = [Tags.Ice, Tags.Construct]
	unit.resists[Tags.Poison] = 100
	unit.resists[Tags.Ice] = 75
	unit.resists[Tags.Physical] = 25
	unit.resists[Tags.Fire] = -50
	return unit

class FrostPunch(Spell):

	def __init__(self):
		Spell.__init__(self)
		self.name = "Frost Punch"
		self.range = 1.5
		self.melee = True
		self.damage = 4
		self.description = "Deals [ice:ice] and [physical:physical] - 1 damage".format(**self.fmt_dict())

	def cast_instant(self, x, y):
		self.caster.level.deal_damage(x, y, self.get_stat('damage'), Tags.Ice, self)
		self.caster.level.deal_damage(x, y, self.get_stat('damage')-1, Tags.Physical, self)
