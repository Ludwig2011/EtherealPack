
from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherealnessBuff(Buff):
	def __init__(self, team=None):
		Buff.__init__(self)
		self.name = "Ätherealness"
		self.team = team
		self.buff_type = BUFF_TYPE_CURSE
		self.stack_type	= STACK_DURATION
		#self.asset = ['EtherealPack', 'status', 'Ätherealness']
		self.description = "Partially shifts unit into the [Äther:äthereal] increasing [physical:physical] resistance by 25% and decreasing [äthereal:äthereal] resistance by 50%.\n lose 10% duration rounded down each round"
		self.color = Ethereal.color
 
	def on_applied(self, owner):
		if self.team == None:
			player = [u for u in self.owner.level.units if u.is_player_controlled][0]
			self.team = player.team
		if not owner.team==self.team:
			if owner.resists[Ethereal] >= 100:
				return ABORT_BUFF_APPLY
			owner.resists[Ethereal] -= 50
			owner.resists[Tags.Physical] += 25
			self.owner = owner
		else:
			owner.resists[Tags.Physical] += 25

	def on_advance(self):
		self.turns_left -= math.floor(self.turns_left/10)

	def on_unapplied(self):
		if not self.owner.team==self.team:
			self.owner.resists[Ethereal] += 50
		self.owner.resists[Tags.Physical] -= 25