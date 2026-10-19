from Level import Equipment, Tags
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherLord(Equipment):

	def on_init(self):
		self.name = "Äther Lord"
		self.tags = [Ethereal]
		self.asset = ['EtherealPack', 'ether_lord']
		self.recipe = [(Ethereal, 2), (Tags.Any, 6)]

		self.tag_bonuses[Ethereal]['max_charges'] = 1
		self.tag_bonuses[Ethereal]['radius'] = 2
		self.tag_bonuses[Ethereal]['range'] = 3
		self.tag_bonuses[Ethereal]['duration'] = 4
		
	def on_init(self):
		self.resists[Ethereal] = 75