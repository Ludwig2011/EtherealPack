from CommonContent import SimpleMeleeAttack
from Level import *
from mods.EtherealPack.models.minions.ether_beam import EtherBeam
from mods.EtherealPack.tags.Ethereal import Ethereal

class LostHeadsBuff(Buff):
	def __init__(self, elemental, damage):
		Buff.__init__(self)
		self.elemental = elemental
		self.name = "Lost Heads"
		self.buff_type = BUFF_TYPE_PASSIVE
		self.stack_type	= STACK_NONE
		self.color = Ethereal.color
		self.global_triggers[EventOnDamaged] = self.on_damaged
		self.damage = damage
		self.stored_damage = 0
	
	def on_damaged(self, evt):
		if evt.unit == self.owner:
			self.stored_damage += evt.damage
			if self.stored_damage > 15:
				self.stored_damage -= 15
				head = Unit()
				head.sprite.char = 'D'
				head.sprite.color = Color(1,121,111)
				head.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
				head.name = "Äther Hydra Head"
				head.description = "Fires äther beam"
				head.max_hp = 15
				head.stationary = True
				head.spells.append(EtherBeam(self.elemental,self.damage))
				head.spells.append(SimpleMeleeAttack(3))
				head.resists[Ethereal] = 100
				head.resists[Tags.Arcane] = -50
				head.tags = [Tags.Dragon, Tags.Living, Ethereal]
				head.team = self.owner.team
				self.summon(head, Point(evt.unit.x, evt.unit.y), 5)