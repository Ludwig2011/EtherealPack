from CommonContent import Poison, SimpleMeleeAttack
from Upgrades import Upgrade
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

class Etherpredators(Upgrade):
	def __init__(self):
		Upgrade.__init__(self)
		self.name = "Äther Predators"
		self.level = 6
		self.tags = [Ethereal, Tags.Nature]
		self.asset = ['EtherealPack', 'skill', 'Ätherpredators']
		self.global_triggers[EventOnMoved] = self.on_moved
		self.minion_damage = 7
		self.minion_health = 14
		self.minion_range = 7
		self.spider_amount = 3

	def get_description(self):
		return ("Enemies that dare jump through space get ambushed by ether spiders.\n"
				"Ether spiders have {minion_health} hp, 2 shields and have teleport attacks with {minion_range} range that deal [{minion_damage}_äthereal:äthereal] damage and apply [poison:poison] aswell as [ätherealness:äthereal] for 7 turns\n"
				"Most forms of movement other than a unit's movement action count as jumping through space.\n"
				"Summon at most 3 spiders per turn").format(**self.fmt_dict())

	def on_advance(self):
		self.spider_amount = 3
		return super().on_advance()

	def on_moved(self, evt):
		if not evt.teleport or not are_hostile(evt.unit, self.owner) or self.spider_amount < 1:
			return
		self.spider_amount -= 1
		self.summon(EtherSpider(self.get_stat('minion_health'), self.get_stat('minion_damage'), self.get_stat('minion_range')), evt.unit)

def EtherSpider(health, damage, range):
	unit = Unit()
	unit.sprite.char = 'D'
	unit.sprite.color = Color(1,255,188)
	unit.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
	unit.name = "Äther Spider"
	unit.description = "Teleports at enemies"
	unit.max_hp = health
	unit.spells.append(TeleportAttack(damage,range))
	unit.spells.append(SimpleMeleeAttack(damage,Poison,7))
	unit.resists[Ethereal] = 75
	unit.resists[Tags.Poison] = 100
	unit.resists[Tags.Physical] = 50
	unit.resists[Tags.Arcane] = -50
	unit.tags = [Tags.Spider, Tags.Nature, Tags.Living, Ethereal]
	return unit

class TeleportAttack(Spell):

	def __init__(self, damage, range):
		Spell.__init__(self)
		self.damage = damage
		self.damage_type = Ethereal
		self.name = "Teleport Attack"
		self.range = range

	def get_leap_dest(self, x, y):
		target_points = list(self.caster.level.get_adjacent_points(Point(x, y), check_unit=True))
		random.shuffle(target_points)
		for point in target_points:
			if point == Point(x, y):
				continue

			if not self.caster.level.can_move(self.caster, point.x, point.y, teleport=True):
				continue

			return point
		return None		

	def get_description(self):
		fmt = "Applies 7 turns of [poison:poison] and [ätherealness:äthereal]"
		return fmt

	def can_cast(self, x, y):
		return Spell.can_cast(self, x, y) and (self.get_leap_dest(x, y) is not None)
			
	def cast(self, x, y):

		leap_dest = self.get_leap_dest(x, y)
		path = self.caster.level.get_points_in_line(Point(self.caster.x, self.caster.y), Point(leap_dest.x, leap_dest.y), find_clear=False)
		for point in path:
			self.caster.level.leap_effect(point.x, point.y, self.damage_type.color, self.caster)
			yield
		
		self.caster.level.act_move(self.caster, leap_dest.x, leap_dest.y, teleport=True)
		self.caster.level.get_unit_at(x, y).apply_buff(EtherealnessBuff(),7)
		self.caster.level.get_unit_at(x, y).apply_buff(Poison(),7)
		self.caster.level.deal_damage(x, y, self.damage, self.damage_type, self)