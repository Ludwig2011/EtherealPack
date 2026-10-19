import random

from Level import *
from Spells import Orb
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.tags.Ethereal import Ethereal

#TODO make work like old orb spell
class PureEtherSphereBuff(Buff):

	def __init__(self, spell):
		self.spell = spell
		self.discharge_cooldown = 0
		Buff.__init__(self)

	def on_init(self):
		self.name = "Pure Ether Sphere"
		self.color = Ethereal.color

	def on_advance(self):
		orb = self.owner
		level = orb.level
		spell = self.spell
		radius = spell.get_stat('radius')
		duration = spell.get_stat('duration')
		damage = spell.get_stat('minion_damage')

		if spell.get_stat('pure_discharge'):
			if self.discharge_cooldown <= 0:
				targets = [
					unit for unit in level.get_units_in_los(orb)
					if unit != orb and are_hostile(orb, unit) and unit.is_alive()
				]
				for target in random.sample(targets, min(3, len(targets))):
					self.zap(target)
				self.discharge_cooldown = 2
			else:
				self.discharge_cooldown -= 1

		self.spread_ether(orb.x, orb.y, radius, duration, damage)

	def zap(self, target):
		spell = self.spell
		level = self.owner.level
		target.apply_buff(Stun(), 2)
		self.spread_ether(target.x, target.y, spell.get_stat('radius'), spell.get_stat('duration'), spell.get_stat('minion_damage'))
		for point in level.get_points_in_line(self.owner, target, find_clear=True)[1:-1]:
			level.show_effect(point.x, point.y, Ethereal, minor=True)

	def spread_ether(self, x, y, radius, duration, damage):
		level = self.owner.level
		for point in level.get_points_in_ball(x, y, radius, diag=True):
			if level.tiles[point.x][point.y].prop is not None:
				continue
			hazard = PureEther(self.spell.caster, self.spell, duration, damage, level.tiles[point.x][point.y].is_chasm)
			level.add_obj(hazard, point.x, point.y)


class PureEtherSphere(Spell):

	def on_init(self):
		self.name = "Pure Ether Sphere"
		self.asset = ['EtherealPack', 'pure_ether_sphere_spell']
		self.minion_damage = 5
		self.range = 9
		self.radius = 1
		self.max_charges = 3
		self.pure_discharge = 0
		self.duration = 7
		self.must_target_empty = True
		self.minion_health = 15
		self.element = Ethereal
		self.damage_type = [Ethereal]
		self.tags = [Ethereal, Tags.Orb, Tags.Conjuration]
		self.level = 4

		self.upgrades['range'] = (5, 2)
		self.upgrades['max_charges'] = (4, 2)
		self.upgrades['radius'] = (1, 2)
		self.upgrades['minion_damage'] = (9, 3)
		self.upgrades['pure_discharge'] = (1, 4, "Pure Discharge", "Every 3 turns, the sphere stuns up to 3 enemies in line of sight for 2 turns and spreads Pure Ether around them.")

	def make_orb(self):
		orb = Orb()
		orb.name = "Pure Ether Sphere"
		orb.asset = ["EtherealPack", "pure_ether_sphere"]
		orb.resists[Ethereal] = 0
		orb.shields = 3
		orb.buffs.append(PureEtherSphereBuff(self))
		apply_minion_bonuses(self, orb)
		return orb

	def cast(self, x, y):
		existing = next((unit for unit in self.caster.level.units if unit.source is self and unit.is_alive()), None)
		if existing:
			if self.caster.level.can_move(existing, x, y, teleport=True):
				self.caster.level.act_move(existing, x, y, teleport=True)
		else:
			self.summon(self.make_orb(), target=Point(x, y))
		yield

	def get_extra_examine_tooltips(self):
		return [self.make_orb()] + self.get_upgrade_tooltips()

	def get_description(self):
		return ("Summon a Pure Ether Sphere at the target location.\n"
				"Each turn, it spreads Pure Ether across a [{radius}:radius] radius, dealing [{minion_damage}_Ethereal:äthereal] damage and applying Etherealness for [{duration}:duration] turns.\n"
				"Only one sphere may exist at a time. Casting the spell while it exists moves it to the selected location.").format(**self.fmt_dict())