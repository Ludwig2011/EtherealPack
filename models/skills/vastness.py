from Upgrades import Upgrade

#skill etherealnessed units loose ice resist and death nova ice and freeze
class Vastness(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Vastness"
		self.asset = ['EtherealPack', 'skill', 'Vastness']