from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

class Ethertuned(Equipment):

	def on_init(self):
		self.name = "Äthertuned"
		self.asset = ['EtherealPack', 'etherealness']
		self.tags = [Ethereal, Tags.Enchantment]
		self.recipe = [(Ethereal, 1), (Tags.Enchantment, 1), (Tags.Any, 2)]

	def get_description(self):
		return "When [Ätherealness:äthereal] is applied to allies, it grants [50% Physical:physical], [50% Äthereal:äthereal], and [100% Poison:poison] resistance for its duration."
