#leaves trail of pure ether hazards, upgrade bolts that stun and spawn pure ether hazards
from Level import *
from Spells import OrbSpell
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.tags.Ethereal import Ethereal


class PureEtherSphere(OrbSpell):

	def on_init(self):
		self.name = "Pure Ether Sphere"
		self.minion_damage = 5
		self.range = 9
		self.radius = 1
		self.max_charges = 3
		self.pure_discharge = 0
		self.duration = 7
		self.zap_cooldwon = 0

		self.melt_walls = True

		self.minion_health = 15

		self.element = Ethereal
		
		self.tags = [Ethereal, Tags.Orb, Tags.Conjuration]
		self.level = 4

		self.upgrades['range'] = (5, 2)
		self.upgrades['max_charges'] = (4, 2)
		self.upgrades['radius'] = (1, 2)
		self.upgrades['minion_damage'] = (9, 3)
		self.upgrades['pure_discharge'] = (1, 4, "Pure Discharge", "The sphere shoots out 3 ether bolts at random targets in line of sight every 3 turns. Stunning them for 2 turns and spreading pure ether on and around them.")

	def zap(self, orb, target):
		target.apply_buff(Stun(),2)
		for stage in Burst(self.caster.level, Point(target.x, target.y), self.get_stat('radius'), expand_diagonals=True):
			for point in stage:
				pure_ether = PureEther(self.caster,self,self.get_stat('duration'),self.get_stat('minion_damage'),self.caster.level.tiles[point.x][point.y].is_chasm)
				if self.caster.level.tiles[point.x][point.y].prop == None:
					self.caster.level.add_obj(pure_ether, point.x, point.y)
			for p in self.caster.level.get_points_in_line(orb, Point(target.x, target.y), find_clear=True)[1:-1]:
				self.caster.level.show_effect(p.x, p.y, Ethereal, minor=True)

	def on_orb_walk(self, existing):
		# Burst
		x = existing.x
		y = existing.y

		if self.get_stat('pure_discharge'):
			if self.zap_cooldwon < 1:
				targets = [u for u in self.level.get_units_in_los(existing) if u != self.caster and u != self.existing and are_hostile(self.caster, u) and u.cur_hp>0]
				if not len(targets) == 0:
					target = random.choice(targets)
					self.zap(existing, target)
					targets.remove(target)
					if not len(targets) == 0:
						target = random.choice(targets)
						self.zap(existing, target)
						targets.remove(target)
						if not len(targets) == 0:
							target = random.choice(targets)
							self.zap(existing, target)
					self.zap_cooldwon = 2
			else:
				self.zap_cooldwon -= 1

		for stage in Burst(self.caster.level, Point(x, y), self.get_stat('radius')):
			for point in stage:
				if self.caster.level.tiles[point.x][point.y].prop == None:
					pure_ether = PureEther(self.caster,self,self.get_stat('duration'),self.get_stat('minion_damage'),self.caster.level.tiles[point.x][point.y].is_chasm)
					self.caster.level.add_obj(pure_ether, point.x, point.y)
			for i in range(3):
				yield
		
		existing.kill()
		self.caster.level.act_move(self.caster, x, y, teleport=True)

	def on_make_orb(self, orb):
		orb.resists[Ethereal] = 0
		orb.asset = ["EtherealPack", "ether_hydra"]
		orb.shields = 3

	def on_orb_move(self, orb, next_point):
		x = next_point.x
		y = next_point.y
		level = orb.level

		if self.get_stat('pure_discharge'):
			if self.zap_cooldwon < 1:
				targets = [u for u in level.get_units_in_los(orb) if u != self.caster and u != orb and are_hostile(self.caster, u) and u.cur_hp>0]
				if not len(targets) == 0:
					target = random.choice(targets)
					self.zap(orb, target)
					targets.remove(target)
					if not len(targets) == 0:
						target = random.choice(targets)
						self.zap(orb, target)
						targets.remove(target)
						if not len(targets) == 0:
							target = random.choice(targets)
							self.zap(orb, target)
					self.zap_cooldwon = 2
			else:
				self.zap_cooldwon -= 1

		for stage in Burst(self.caster.level, Point(x, y), self.get_stat('radius'), expand_diagonals=True):
			for point in stage:
				if self.caster.level.tiles[point.x][point.y].prop == None:
					pure_ether = PureEther(self.caster,self,self.get_stat('duration'),self.get_stat('minion_damage'),self.caster.level.tiles[point.x][point.y].is_chasm)
					self.caster.level.add_obj(pure_ether, point.x, point.y)

	def on_orb_collide(self, orb, next_point):
		orb.level.show_effect(next_point.x, next_point.y, Ethereal)
		yield

	def get_orb_impact_tiles(self, orb):
		return [p for stage in Burst(self.caster.level, orb, self.get_stat('radius')) for p in stage]

	def get_description(self):
		return ("Summon a Pure Ether Sphere next to the caster.\n"
				"The sphere spreads pure ether each turn to all adjacent tiles that deals [{minion_damage}_äthereal:äthereal] damage, applies [Atherealness:äthereal] for 2 turns and lasts 7 turns.\n"
				"The orb has no will of its own, each turn it will float one tile towards the target and destroy walls in its path.\n"
				"The orb can be destroyed by [äthereal:äthereal] damage.").format(**self.fmt_dict())