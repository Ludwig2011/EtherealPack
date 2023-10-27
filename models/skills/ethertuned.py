from Level import *
from Upgrades import Upgrade
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

#skill when ally ethereal heal instead of dmg
class Ethertuned(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Äthertuned"
		#self.asset = ['EtherealPack', 'skill', 'Äthertuned']
		self.tags = [Ethereal]

		self.level = 4
