
from Level import *
from mods.EtherealPack.models.buffs.hex_buffs import HexBuff, HexDebuff
from mods.EtherealPack.tags.Ethereal import Ethereal

class Hex(Spell):
	def on_init(self):
		self.name = "Hex"
		self.range = 10 
		self.tags = [Ethereal, Tags.Dark, Tags.Enchantment]
		self.level = 2

		self.duration = 7
		self.damage = 3
		self.damage_types = [Ethereal, Tags.Dark]
		self.resist_loss = 25

		self.max_charges = 7

		self.upgrades['damage'] = (4, 3)
		self.upgrades['resist_loss'] = (25, 2)
		self.upgrades['range'] = (4, 1)
		self.upgrades['deterioration'] = (1, 3, "Deterioration", "Targets effected by hex also lose [physical_physical:physical], [poison_poison:poison]poison and [ice_ice:ice] resistance".format(**self.fmt_dict()))
		self.upgrades['volatile_death'] = (1, 4, "Volatile Death", "When a target effected by Hex dies, cause an explosion with [5_tile:radius] dealing [7_dark:dark] and [7_äthereal:äthereal] damage".format(**self.fmt_dict()))
		self.upgrades['perpetual_curse'] = (1, 6, "Perpetual Curse", "When a target effected by both Hex dies, reaply Hex to a random enemy in line of sight.")
		

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		unit.apply_buff(HexDebuff(self.get_stat('resist_loss'), self.get_stat('deterioration')), self.get_stat('duration'))
		self.caster.apply_buff(HexBuff(self.get_stat('damage'), self.get_stat('volatile_death'), self.get_stat('perpetual_curse'), self.get_stat('resist_loss'), self.get_stat('deterioration'), self.get_stat('duration')), self.get_stat('duration'))
		yield
		
	def get_description(self):
		return "Curse enemy to take [{damage}_äthereal:äthereal] and [{damage}_dark:dark] damage whenever they take damage.".format(**self.fmt_dict())
