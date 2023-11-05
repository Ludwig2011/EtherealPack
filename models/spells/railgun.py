#charge railgun cast -> gain charge buff every turn and change name to fire railgun
#fire railgun cast -> change name back and has range and damage based on turns charged(buff duration goes up instead of down?) and gets rid of buff
# max pool of damage that gets reduced per unit hit? to a max per unit?
# damage in straight line, ?destroy walls based on charge or upgrade?
# charge speed upgrade

from Level import *
from mods.EtherealPack.models.buffs.hex_buffs import HexBuff, HexDebuff
from mods.EtherealPack.tags.Ethereal import Ethereal

class Railgun(Spell):
	def on_init(self):
		self.name = "Railgun"
		self.range = 0 
		self.tags = [Ethereal, Tags.Metallic, Tags.Scorcery]
		self.level = 2

		self.damage = 5
		self.damage_types = [Ethereal, Tags.Physical]

		self.max_charges = 7
		self.charge_speed = 7

		self.upgrades['charge_speed'] = (1, 3)
		self.upgrades['deterioration'] = (1, 2, "Deterioration", "[äthereal:äthereal][physical:physical]".format(**self.fmt_dict()))
		

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		unit.apply_buff(HexDebuff(self.get_stat('resist_loss'), self.get_stat('deterioration')), self.get_stat('duration'))
		self.caster.apply_buff(HexBuff(self.get_stat('damage'), self.get_stat('volatile_death'), self.get_stat('perpetual_curse'), self.get_stat('resist_loss'), self.get_stat('deterioration'), self.get_stat('duration')), self.get_stat('duration'))
		yield

	def can_cast(self, x, y):
		return self.caster.level.get_unit_at(x, y) and Spell.can_cast(self, x, y)
		
	def get_description(self):
		return "Curse enemy to take [{damage}_äthereal:äthereal] and [{damage}_dark:dark] damage whenever they take damage for [{duration}_turns:duration].".format(**self.fmt_dict())
