from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherEyeBuff(Buff):

	def __init__(self, damage, freq, requires_los, spell): # spell = source?
		Buff.__init__(self)
		self.name = "Eye of Äther"
		self.color = Ethereal.color
		self.requires_los = requires_los
		self.asset = ['status', 'ice_eye']	
		self.damage_type = Ethereal
		self.damage = damage
		self.freq = freq
		self.cooldown = freq
		self.name = "Elemental Eye"

	def on_advance(self):

		self.cooldown -= 1
		if self.cooldown == 0:
			self.cooldown = self.freq


			possible_targets = self.owner.level.units
			possible_targets = [t for t in possible_targets if self.owner.level.are_hostile(t, self.owner)]
			if self.requires_los:
				possible_targets = [t for t in possible_targets if self.owner.level.can_see(t.x, t.y, self.owner.x, self.owner.y)]

			if possible_targets:
				target = random.choice(possible_targets)
				self.owner.level.queue_spell(self.shoot(Point(target.x, target.y)))
				self.cooldown = self.freq
			else:
				self.cooldown = 1


	def shoot(self, target):
		path = self.owner.level.get_points_in_line(Point(self.owner.x, self.owner.y), target, find_clear=self.requires_los)

		for point in path:
			self.owner.level.deal_damage(point.x, point.y, 0, self.damage_type, self)
			yield

		self.owner.level.deal_damage(target.x, target.y, self.damage, self.damage_type, self)


class EyeOfEtherSpell(Spell):

	def on_init(self):
		self.range = 0
		self.max_charges = 4
		self.name = "Eye of Äther"
		self.requires_los = True
		self.damage = 15
		self.element = Ethereal
		self.duration = 30
		self.shot_cooldown = 3
		
		self.upgrades['shot_cooldown'] = (-1, 1)
		self.upgrades['duration'] = 15
		self.upgrades['damage'] = (7, 2)
		self.upgrades['requires_los'] = (-1, 1)

		self.tags = [Ethereal, Tags.Enchantment, Tags.Eye]
		self.level = 2

	def cast_instant(self, x, y):
		buff = EtherEyeBuff(self.get_stat('damage'), self.get_stat('shot_cooldown'), self.get_stat('requires_los'), self)
		buff.element = self.element
		self.caster.apply_buff(buff, self.get_stat('duration'))

	def get_description(self):
		return ("Every [{shot_cooldown}_turns:shot_cooldown], deals [{damage}_äthereal:äthereal] damage to a random enemy unit in line of sight.\n"
				"Lasts [{duration}_turns:duration].").format(**self.fmt_dict())