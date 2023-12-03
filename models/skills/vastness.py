from Level import *
from Upgrades import Upgrade
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

#skill etherealnessed units loose ice resist and death nova ice and freeze
class Vastness(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Vastness"
		#self.asset = ['EtherealPack', 'Vastness']
		self.tags = [Ethereal, Tags.Ice]
		self.global_triggers[EventOnDamaged] = self.on_damaged
		self.radius = 4
		self.damage = 7
		self.level = 6

	def on_damaged(self, damage_event):

		if not self.owner.level.are_hostile(self.owner, damage_event.unit):
			return

		if damage_event.unit.cur_hp <= 0 and damage_event.unit.has_buff(EtherealnessBuff):
			for point in self.owner.level.get_points_in_ball(damage_event.unit.x, damage_event.unit.y, self.radius):
				unit = self.owner.level.get_unit_at(point.x, point.y)
				if unit and are_hostile(self.owner,unit):
					self.owner.level.deal_damage(point.x, point.y, self.damage, Tags.Ice, self)
					self.owner.level.deal_damage(point.x, point.y, self.damage, Ethereal, self)
					if unit.cur_hp > 0:
						unit.apply_buff(EtherealnessBuff(), 7)
				else:
					self.owner.level.show_effect(point.x, point.y, Ethereal)
			
		
	def get_description(self):
		return ("Enemies that are [ätherealised:äthereal] lose 50% [ice:ice] resistance.\n"
				"When an [ätherealised:äthereal] enemy dies cause an nova in a [4_tile:radius] radius dealing 7 [ätheral:äthereal] and [ice:ice] damage to enemies.").format(**self.fmt_dict())
