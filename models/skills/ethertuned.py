from Level import *
from Upgrades import Upgrade
from mods.EtherealPack.tags.Ethereal import Ethereal

class Ethertuned(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Äthertuned"
		#self.asset = ['EtherealPack', 'skill', 'Äthertuned']
		self.tags = [Ethereal]
		self.description = "When Ätherealness is applied to allies it increases their phyiscal and äthereal resistance by 50 aswell as their poison resistane by 100"
		self.level = 4
