
class EtherealnessBuff(Level.Buff):#cant meele? #stackable? #still applied/effect 100 resists?
	def __init__(self):
		Level.Buff.__init__(self)
		self.name = "Ätherealness"
		self.buff_type = Level.BUFF_TYPE_CURSE
		self.stack_type	= Level.STACK_NONE
		self.asset = ['EtherealPack', 'status', 'Ätherealness']
		self.color = Level.Tags.Ethereal.color
	
	def on_applied(self, owner):
		if owner.resists[Level.Tags.Ethereal] >= 100:
			return Level.ABORT_BUFF_APPLY
		owner.resists[Level.Tags.Ethereal] -= 50
		owner.resists[Level.Tags.Physical] += 25