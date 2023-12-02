from Level import Upgrade
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherLord(Upgrade):

	def on_init(self):
		self.name = "Äther Lord"
		self.tags = [Ethereal]
		self.asset = ['EtherealPack', 'ether_lord']

		self.tag_bonuses[Ethereal]['max_charges'] = 3
		self.tag_bonuses[Ethereal]['duration'] = 2
		self.tag_bonuses[Ethereal]['radius'] = 1

		self.level = 7