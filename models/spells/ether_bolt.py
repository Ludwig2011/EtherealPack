from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherBolt(Spell):

	def on_init(self):
		self.name = "Äther Bolt"
		self.range = 8 
		self.tags = [Ethereal, Tags.Sorcery]
		self.level = 1

		self.damage = 11
		self.duration = 3
		self.damage_type = Ethereal

		self.max_charges = 10 
		self.shield_burn = 0

		self.upgrades['max_charges'] = (15, 2)
		self.upgrades['damage'] = (10, 3)
		self.upgrades['range'] = (5, 1)
		self.upgrades['energy_drain'] = (5, 2, "Energy Drain", "If Äther Bolt targets a unit affected by Ätherealness, it grants you a shield up to maximum of 5")
		self.upgrades['energy_disruption'] = (1, 4, "Energy Disruption", "If Äther Bolt targets a unit affected by Ätherealness, it deals %d [fire], [lightning], and [ice] aswell" % (self.damage/2))
		self.upgrades['energy_connection'] = (1, 6, "Energy Connection", "If Äther Bolt targets a unit affected by Ätherealness, Äther Bolt is cast again at units affected by Ätherealness in line of sight.")


	def cast(self, x, y, connected=True):
		dtypes = []
		unit = self.caster.level.get_unit_at(x, y)

		for p in self.caster.level.get_points_in_line(self.caster, Level.Point(x, y), find_clear=True)[1:-1]:
			self.caster.level.show_effect(p.x, p.y, Ethereal, minor=True)

		if unit:
			if unit.has_buff(EtherealnessBuff):
				if self.get_stat('energy_drain'):
						if self.caster.shields < self.get_stat('energy_drain'):
							self.caster.shields += 1
				if self.get_stat('energy_disruption'):
					dtypes = [Tags.Fire, Tags.Lightning, Tags.Ice]
				if self.get_stat('energy_connection') and connected:
					for u in self.caster.level.get_units_in_los(unit):
						if u.has_buff(EtherealnessBuff):
							self.caster.level.deal_damage(u.x, u.y, self.get_stat('damage'), Ethereal, self)
							for dtype in dtypes:
								self.caster.level.deal_damage(u.x, u.y, self.get_stat('damage')/2, dtype, self)
							if u and u.resists[Ethereal] < 100:
								u.apply_buff(EtherealnessBuff(), self.get_stat('duration'))

		self.caster.level.deal_damage(x, y, self.get_stat('damage'), Ethereal, self)
		for dtype in dtypes:
			self.caster.level.deal_damage(x, y, self.get_stat('damage')/2, dtype, self)
		if unit and unit.resists[Ethereal] < 100:
			unit.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
		yield

	def get_description(self):
		return "Deal [{damage}_äthereal:äthereal] damage to the target and apply Ätherealness for [{duration}_turns:duration].".format(**self.fmt_dict())