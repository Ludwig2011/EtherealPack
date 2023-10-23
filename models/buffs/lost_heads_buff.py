
class LostHeadsBuff(Level.Buff):
	def __init__(self, elemental):
		Level.Buff.__init__(self)
		self.elemental = elemental
		self.name = "Lost Heads"
		self.buff_type = Level.BUFF_TYPE_PASSIVE
		self.stack_type	= Level.STACK_NONE
		self.color = Ethereal.color
		self.global_triggers[EventOnDamaged] = self.on_damaged
		self.stored_damage = 0
	
	def on_damaged(self, evt):
		self.stored_damage += evt.damage
		if self.stored_damage > 15:
			self.stored_damage -= 15
			head = Level.Unit()
			head.sprite.char = 'D'
			head.sprite.color = Color(1,121,111)
			head.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
			head.name = "Äther Hydra Head"
			head.description = "Fires äther beam"
			head.max_hp = 15
			head.stationary = True
			head.spells.append(EtherBeam(self.elemental))
			head.spells.append(SimpleMeleeAttack(3))
			head.resists[Ethereal] = 100
			head.resists[Tags.Arcane] = -50
			head.tags = [Tags.Dragon, Tags.Living, Ethereal]
			head.team = self.owner.team
			self.summon(head, Point(evt.unit.x, evt.unit.y), 5)