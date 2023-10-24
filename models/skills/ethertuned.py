from Upgrades import Upgrade

#skill when ally ethereal heal instead of dmg
class Ethertuned(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Äthertuned"
		self.asset = ['EtherealPack', 'skill', 'Äthertuned']