
from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherealnessBuff(Buff):
	def __init__(self):
		Buff.__init__(self)
		self.name = "Ätherealness"
		self.buff_type = BUFF_TYPE_CURSE
		self.stack_type	= STACK_DURATION
		self.ethertuned = False
		self.vastness = False
		self.ally = False
		self.player = None
		self.asset = ['EtherealPack', 'etherealness']
		self.description = "Partially shifts unit into the [Äther:äthereal] increasing [physical:physical] resistance by 25% and decreasing [äthereal:äthereal] resistance by 50%.\n Lose 10% duration rounded down each round.\n Äther and 100% [äthereal:äthereal] resistant units are immune"
		self.color = Ethereal.color
 
	def on_applied(self, owner):
		if self.player == None:
			self.player = [u for u in self.owner.level.units if u.is_player_controlled][0]
		for skill in self.player.get_skills():
			if skill.name == "Äthertuned":
				self.ethertuned = True
		for skill in self.player.get_skills():
			if skill.name == "Vastness":
				self.vastness = True
		team = self.player.team
		if owner.team==team and self.ethertuned:
			owner.resists[Tags.Physical] += 50
			owner.resists[Ethereal] += 50
			owner.resists[Tags.Poison] += 100
			self.ally = True
		else:
			if owner.resists[Ethereal] >= 100 or Ethereal in owner.tags:
				return ABORT_BUFF_APPLY
			
			if self.vastness:
				owner.resists[Tags.Ice] -= 50
			owner.resists[Ethereal] -= 50
			owner.resists[Tags.Physical] += 25
			self.owner = owner

	def on_advance(self):
		self.turns_left -= math.floor(self.turns_left/10)

	def on_unapplied(self):
		if self.ally:
			self.owner.resists[Tags.Physical] -= 50
			self.owner.resists[Ethereal] -= 50
			self.owner.resists[Tags.Poison] -= 100
		else:
			self.owner.resists[Ethereal] += 50
			self.owner.resists[Tags.Physical] -= 25
			if self.vastness:
				self.owner.resists[Tags.Ice] += 50