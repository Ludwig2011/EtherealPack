from Level import *
from Upgrades import Upgrade
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherGigantism(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Äther Gigantism"
		#self.asset = ['EtherealPack', 'ether_gigantism']
		self.tags = [Ethereal, Tags.Nature]
		self.description = "Every turn an ally spends in stasis they grow larger, gaining 2 minion damage and 5 hp"
		self.level = 4
