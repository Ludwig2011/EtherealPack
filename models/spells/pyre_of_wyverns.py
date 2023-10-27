from Level import *
from mods.EtherealPack.models.minions.ether_wyvern import EtherWyvern
from mods.EtherealPack.tags.Ethereal import Ethereal 

class PyreOfWyvernsSpell(Spell):

	def on_init(self):

		self.name = "Pyre of Wyverns"

		self.minion_health = 10
		self.minion_damage = 6
		self.minion_range = 5
		self.num_summons = 3
		self.shields = 2

		self.max_charges = 2
		self.upgrades['ether_link'] = 1, 4, "Ether Link", "wyverns link up to each other providing shield regeneration if they stay within certain range"

		self.range = 0

		self.level = 5
		self.tags = [Tags.Dragon, Tags.Living, Ethereal]



	def get_description(self):
		return ("Summons [{num_summons}_wyverns:num_summons] near the caster.\n"
				"Wyverns have [{minion_health}_HP:minion_health].\n"
				"Wyverns have a melee attack which deals [{minion_damage}_physical:physical] damage.").format(**self.fmt_dict())

	def cast_instant(self, x, y):
		for i in range(self.get_stat('num_summons')):

			wyvern = EtherWyvern(shields=self.get_stat('shields'), ether_link=True if self.get_stat('ether_link') else False)
			wyvern.team = self.caster.team 


			self.summon(wyvern, Point(x, y))