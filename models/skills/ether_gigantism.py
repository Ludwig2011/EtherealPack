from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherGigantism(Equipment):

	def on_init(self):
		self.name = "Äther Gigantism"
		self.asset = ['EtherealPack', 'bliss_stasis']
		self.tags = [Ethereal, Tags.Nature]
		self.recipe = [(Ethereal, 1), (Tags.Nature, 1), (Tags.Conjuration, 1), (Tags.Any, 1)]

	def get_description(self):
		return "Each turn an allied unit remains in Ethereal stasis, it gains 5 max HP and its spells with damage gain 2 damage."
