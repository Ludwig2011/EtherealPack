
class Hex(Level.Spell): # to weak -> radius or stun?
	def on_init(self):
		self.name = "Hex"
		self.range = 10 
		self.tags = [Ethereal, Tags.Dark, Tags.Enchantment]
		self.level = 2

		self.duration = 7
		self.damage = 3
		self.damage_types = [Ethereal, Tags.Dark]

		self.max_charges = 7

		self.upgrades['damage'] = (4, 3)
		self.upgrades['range'] = (4, 1)
		self.upgrades['energy_disruption'] = (1, 4, "Volatile Death", "When a target effected by Hex dies, cause an explosion with [{radius}_tile:radius] ".format(**self.fmt_dict()))
		self.upgrades['perpetual_curse'] = (1, 6, "Perpetual Curse", "When a target effected by both Hex and Ätherealness dies, reaply Hex to a random enemy in line of sight.")
		

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		unit.apply_buff(HexBuff(self.get_stat('damage'), self.get_stat('energy_disruption'), self.get_stat('perpetual_curse')), self.get_stat('duration'))

	def get_description(self):
		return "Deal [{damage}_äthereal:äthereal] damage to the target.".format(**self.fmt_dict())
