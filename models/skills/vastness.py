from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

#skill etherealnessed units loose ice resist and death nova ice and freeze
class Vastness(Equipment):

	def on_init(self):
		self.name = "Vastness"
		self.asset = ['EtherealPack', 'pure_ether']
		self.tags = [Ethereal, Tags.Ice, Tags.Enchantment]
		self.recipe = [(Ethereal, 2), (Tags.Ice, 2), (Tags.Enchantment, 2), (Tags.Any, 2)]
		self.global_triggers[EventOnDamaged] = self.on_damaged
		self.radius = 3
		self.damage = 7
		self.duration = 1

	def on_damaged(self, damage_event):

		if not self.owner.level.are_hostile(self.owner, damage_event.unit):
			return

		if damage_event.unit.cur_hp <= 0 and damage_event.unit.has_buff(EtherealnessBuff):
			for point in self.owner.level.get_points_in_ball(damage_event.unit.x, damage_event.unit.y, self.get_stat('radius')):
				unit = self.owner.level.get_unit_at(point.x, point.y)
				if unit and are_hostile(self.owner,unit):
					self.owner.level.deal_damage(point.x, point.y, self.get_stat('damage'), Tags.Ice, self)
					self.owner.level.deal_damage(point.x, point.y, self.get_stat('damage'), Ethereal, self)
					if unit.cur_hp > 0:
						unit.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
				else:
					self.owner.level.show_effect(point.x, point.y, Ethereal)
			
		
	def get_description(self):
		return "Etherealness lowers affected enemies' Ice resistance by 50. When an affected enemy dies, deal 7 Ice and Ethereal damage to hostile units in a 4-tile radius and apply 7 turns of Etherealness to survivors."
