
from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

#watch out that not all buffs check for damage event (check self? or give caster permanent positive buff that checks event)
# apply this to an invisible unit or passivly to caster or register damage event on spell and not on buff
class HexBuff(Buff):
	def __init__(self,damage,volatile_death,perpetual_curse, resist_loss, deterioration, duration):
		Buff.__init__(self)
		self.name = "Hexer"
		self.buff_type = BUFF_TYPE_BLESS
		self.stack_type	= STACK_REPLACE
		self.damage = damage
		self.color = Ethereal.color
		self.global_triggers[EventOnDamaged] = self.on_damaged
		self.volatile_death = volatile_death
		self.perpetual_curse = perpetual_curse
		self.resist_loss = resist_loss
		self.deterioration = deterioration
		self.duration = duration

	def on_damaged(self, evt):
		if not evt.source==self and evt.unit and evt.unit.has_buff(HexDebuff):
			self.owner.level.deal_damage(evt.unit.x,evt.unit.y, self.damage, Tags.Dark, self)
			self.owner.level.deal_damage(evt.unit.x,evt.unit.y, self.damage, Ethereal, self)
			if evt.unit.cur_hp <= 0:
				if self.volatile_death:
					for stage in Burst(self.owner.level, evt.unit, 4):
						for point in stage:
							if self.owner.level.get_unit_at(point.x, point.y) and are_hostile(self.owner,self.owner.level.get_unit_at(point.x, point.y)):
								self.owner.level.deal_damage(point.x, point.y, self.damage, Tags.Dark, self)
								self.owner.level.deal_damage(point.x, point.y, self.damage, Ethereal, self)
							else:
								self.owner.level.show_effect(point.x, point.y, Ethereal)
				if self.perpetual_curse:
					targets = self.owner.level.get_units_in_los(evt.unit)
					targets = [t for t in targets if are_hostile(self.owner, t)]
					random.choice(targets).apply_buff(HexDebuff(self.resist_loss, self.deterioration), self.duration)
					self.turns_left = 7
				
class HexDebuff(Buff):
	def __init__(self, loss, deterioration):
		Buff.__init__(self)
		self.buff_type = BUFF_TYPE_CURSE
		self.stack_type	= STACK_REPLACE
		self.name = "Hex"
		self.color = Ethereal.color
		self.loss = loss
		self.deterioration = deterioration
	
	def on_applied(self, owner):
		if owner.resists[Ethereal] >= 100:
			return ABORT_BUFF_APPLY
		owner.resists[Ethereal] -= self.loss
		owner.resists[Tags.Dark] -= self.loss
		if (self.deterioration):
			owner.resists[Tags.Physical] -= self.loss
			owner.resists[Tags.Poison] -= self.loss
			owner.resists[Tags.Ice] -= self.loss
		self.owner = owner
	
	def on_unapplied(self):
		self.owner.resists[Ethereal] += self.loss
		self.owner.resists[Tags.Dark] += self.loss
		if (self.deterioration):
			self.owner.resists[Tags.Physical] += self.loss
			self.owner.resists[Tags.Poison] += self.loss
			self.owner.resists[Tags.Ice] += self.loss
