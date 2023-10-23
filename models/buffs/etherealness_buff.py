
from Level import *
from mods.EtherealPack.EtherealPack import Ethereal


class EtherealnessBuff(Buff):#cant meele? #stackable? #still applied/effect 100 resists?
	def __init__(self):
		Buff.__init__(self)
		self.name = "Ätherealness"
		self.buff_type = BUFF_TYPE_CURSE
		self.stack_type	= STACK_NONE
		self.asset = ['EtherealPack', 'status', 'Ätherealness']
		self.color = Ethereal.color
	
	def on_applied(self, owner):
		if owner.resists[Ethereal] >= 100:
			return ABORT_BUFF_APPLY
		owner.resists[Ethereal] -= 50
		owner.resists[Tags.Physical] += 25