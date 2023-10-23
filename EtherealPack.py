import os
import random
import Spells
from CommonContent import RegenBuff, SimpleMeleeAttack
import Level, Upgrades
from Level import Bolt, Color, EventOnDamaged, Point, Tags, are_hostile
import mods.API_Universal.Modred as Modred

Ethereal = Level.Tag("Äthereal", Level.Color(1,255,188))
#demons undead dark holy weak, arcane strong (living/nature aswell?)
Level.Tags.elements.append(Ethereal)
Modred.add_tag_keybind(Ethereal, 'Ä')

Etherealness = Level.Tag("Ätherealness", Level.Color(1,255,188))

Modred.add_tag_tooltip(Ethereal)
Modred.add_tag_tooltip(Etherealness)

# Add custom spells
#Modred.add_tag_effect_simple(Ethereal, os.path.join('mods','EtherealPack', ''))

Modred.add_shrine_option(Ethereal, 1)

class EtherealnessBuff(Level.Buff):#cant meele? #stackable? #still applied/effect 100 resists?
	def __init__(self):
		Level.Buff.__init__(self)
		self.name = "Ätherealness"
		self.buff_type = Level.BUFF_TYPE_CURSE
		self.stack_type	= Level.STACK_DURATION
		#self.asset = ['EtherealPack', 'status', 'Ätherealness']
		self.color = Ethereal.color
	
	def on_applied(self, owner):
		if owner.resists[Ethereal] >= 100:
			return Level.ABORT_BUFF_APPLY
		owner.resists[Ethereal] -= 50
		owner.resists[Tags.Physical] += 25	

	def on_unapplied(self, owner):
		owner.resists[Ethereal] += 50
		owner.resists[Tags.Physical] -= 25

#SKILLS

#skill when ally ethereal heal instead of dmg
class Ethertuned(Upgrades.Upgrade):
	def __init__(self):
		Upgrades.Upgrade.__init__(self)
		self.name = "Äthertuned"
		self.asset = ['EtherealPack', 'skill', 'Äthertuned']
		
#skill enemy teleport summon spider
class Etherpredators(Upgrades.Upgrade):
	def __init__(self):
		Upgrades.Upgrade.__init__(self)
		self.name = "Äther Predators"
		self.asset = ['EtherealPack', 'skill', 'Ätherpredators']

#skill etherealnessed units loose ice resist and death nova ice and freeze
class Vastness(Upgrades.Upgrade):
	def __init__(self):
		Upgrades.Upgrade.__init__(self)
		self.name = "Vastness"
		self.asset = ['EtherealPack', 'skill', 'Vastness']

#SPELLS

class EtherBolt(Level.Spell):

	def on_init(self):
		self.name = "Äther Bolt"
		self.range = 8 
		self.tags = [Ethereal, Tags.Sorcery]
		self.level = 1

		self.damage = 11
		self.duration = 3
		self.damage_type = Ethereal

		self.max_charges = 10 

		self.upgrades['max_charges'] = (15, 2)
		self.upgrades['damage'] = (10, 3)
		self.upgrades['range'] = (5, 1)
		self.upgrades['energy_drain'] = (5, 2, "Energy Drain", "If Äther Bolt targets a unit affected by Ätherealness, it grants you a shield up to maximum of 5")
		self.upgrades['energy_disruption'] = (1, 4, "Energy Disruption", "If Äther Bolt targets a unit affected by Ätherealness, it deals %d [fire], [lightning], and [ice] aswell" % (self.damage/2))
		self.upgrades['energy_connection'] = (1, 6, "Energy Connection", "If Äther Bolt targets a unit affected by Ätherealness, Äther Bolt is cast again at units affected by Ätherealness in line of sight.")
		

	def cast(self, x, y, connected=True):
		dtypes = []
		unit = self.caster.level.get_unit_at(x, y)
				
		for p in self.caster.level.get_points_in_line(self.caster, Level.Point(x, y), find_clear=True)[1:-1]:
			self.caster.level.show_effect(p.x, p.y, Ethereal, minor=True)

		if unit:
			if unit.has_buff(EtherealnessBuff):
				if self.get_stat('energy_drain'):
						if self.caster.shields < self.get_stat('energy_drain'):
							self.caster.shields += 1
				if self.get_stat('energy_disruption'):
					dtypes = [Tags.Fire, Tags.Lightning, Tags.Ice]
				if self.get_stat('energy_connection') and connected:
					for u in self.caster.level.get_units_in_los(unit):
						if u.has_buff(EtherealnessBuff):
							self.caster.level.deal_damage(u.x, u.y, self.get_stat('damage'), Ethereal, self)
							for dtype in dtypes:
								self.caster.level.deal_damage(u.x, u.y, self.get_stat('damage')/2, dtype, self)
							if u and u.resists[Ethereal] < 100:
								u.apply_buff(EtherealnessBuff(), self.get_stat('duration'))

		self.caster.level.deal_damage(x, y, self.get_stat('damage'), Ethereal, self)
		for dtype in dtypes:
			self.caster.level.deal_damage(x, y, self.get_stat('damage')/2, dtype, self)
		if unit and unit.resists[Ethereal] < 100:
			unit.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
		yield

	def get_description(self):
		return "Deal [{damage}_äthereal:äthereal] damage to the target and apply Ätherealness for [{duration}_turns:duration].".format(**self.fmt_dict())

class Hex(Level.Spell): # to weak -> radius or stun?
	def on_init(self):
		self.name = "Hex"
		self.range = 10 
		self.tags = [Ethereal, Tags.Dark, Tags.Enchantment]
		self.level = 2

		self.duration = 7
		self.damage = 3
		self.damage_types = [Ethereal, Tags.Dark]

		self.max_charges = 7

		self.upgrades['damage'] = (4, 3)
		self.upgrades['range'] = (4, 1)
		self.upgrades['energy_disruption'] = (1, 4, "Volatile Death", "When a target effected by Hex dies, cause an explosion with [{radius}_tile:radius] ".format(**self.fmt_dict()))
		self.upgrades['perpetual_curse'] = (1, 6, "Perpetual Curse", "When a target effected by both Hex and Ätherealness dies, reaply Hex to a random enemy in line of sight.")
		

	def cast(self, x, y):
		unit = self.caster.level.get_unit_at(x, y)
		unit.apply_buff(HexBuff(self.get_stat('damage'), self.get_stat('energy_disruption'), self.get_stat('perpetual_curse')), self.get_stat('duration'))

	def get_description(self):
		return "Deal [{damage}_äthereal:äthereal] damage to the target.".format(**self.fmt_dict())


class EtherBreath(Level.Spell):
	def __init__(self, elemental):
		Level.Spell.__init__(self)

		self.name = "Äther Breath"
		self.damage = 7
		self.beam = True
		self.cool_down = 7
		self.elemental = elemental

	def get_description(self):
		return "Breaths out three Äther Beams"

	def cast(self, x, y):
		if self.elemental:
			dtypes1 = [Ethereal,Tags.Fire]
			dtypes2 = [Ethereal,Tags.Lightning]
			dtypes3 = [Ethereal,Tags.Ice]
		else:
			dtypes1 = [Ethereal]
			dtypes2 = [Ethereal]
			dtypes3 = [Ethereal]
		start = Point(self.caster.x, self.caster.y)
		target = Point(x, y)

		for point in Bolt(self.caster.level, start, target, find_clear=True):
			self.hit(point.x, point.y, dtypes1)

		target = self.get_ai_target()
		if target:
			for point in Bolt(self.caster.level, start, target, find_clear=True):
				self.hit(point.x, point.y, dtypes2)

		target = self.get_ai_target()
		if target:
			for point in Bolt(self.caster.level, start, target, find_clear=True):
				self.hit(point.x, point.y, dtypes3)
		yield

	def get_impacted_tiles(self, x, y):
		tiles = set()
		tiles.add(Point(x, y))

		target = Point(x, y)

		if self.beam:
			for p in Bolt(self.caster.level, self.caster, target):
				tiles.add(p)

		return tiles				

	def hit(self, x, y, dtypes):
		unit = self.caster.level.get_unit_at(x, y)
		if not unit or are_hostile(self.caster, unit):
			for dtype in dtypes:
				self.caster.level.deal_damage(x, y, self.get_stat('damage'), dtype, self)

def EtherHydra(elemental=False):
	unit = Level.Unit()
	unit.sprite.char = 'D'
	unit.sprite.color = Color(1,255,188)
	unit.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
	unit.name = "Äther Hydra"
	unit.description = "Fires äther beams"
	unit.max_hp = 45
	unit.spells.append(EtherBreath(elemental))
	unit.spells.append(SimpleMeleeAttack(9))
	unit.resists[Ethereal] = 100
	unit.resists[Tags.Arcane] = -50
	unit.tags = [Tags.Dragon, Tags.Living, Ethereal]
	return unit

class SummonEtherHydraSpell(Level.Spell):

	def on_init(self):
		self.name = "Äther Hydra"
		self.range = 4
		self.max_charges = 2
		self.tags = [Ethereal, Tags.Conjuration, Tags.Dragon]
		self.level = 4

		self.minion_health = 45
		self.minion_damage = 8
		self.breath_damage = EtherHydra().spells[0].damage
		self.minion_range = 7
		self.minion_regen = 1
		self.upgrades['minion_health'] = (30, 2)
		self.upgrades['breath_damage'] = (7, 2)
		self.upgrades['minion_regen'] = (1, 1)
		self.upgrades['element_mother'] = (1, 3, "Element Mother", "Each of the Äther Hydras Äther Beams redeals its damage as either fire lightning or ice damage")
		self.upgrades['lost_heads'] = (1, 4, "Lost Heads", "Whenever the hydra loses 15 hp spawn a stationary minion with an äther beam attack nearby")
		self.upgrades['dragon_mage'] = (1, 6, "Dragon Mage", "Summoned Äther Hydras can cast Äther Bolt with a 3 turn cooldown.\nThis Äther Bolt gains all of your upgrades and bonuses.")


		self.must_target_empty = True

	def cast_instant(self, x, y):
		drake = EtherHydra(self.get_stat('element_mother'))
		drake.team = self.caster.team
		drake.max_hp = self.get_stat('minion_health')
		drake.spells[0].damage = self.get_stat('breath_damage')
		drake.spells[0].range = self.get_stat('minion_range')
		drake.spells[1].damage = self.get_stat('minion_damage')

		drake.buffs.append(RegenBuff(self.get_stat('minion_regen')))
		if self.get_stat('lost_heads'):
			drake.buffs.append(LostHeadsBuff(self.get_stat('element_mother')))

		if self.get_stat('dragon_mage'):
			fball = EtherBolt()
			fball.statholder = self.caster
			fball.max_charges = 0
			fball.cur_charges = 0
			fball.cool_down = 3
			drake.spells.insert(1, fball)

		self.summon(drake, Point(x, y))

	def get_description(self):
		return ("Summon an Äther Hydra at target square.\n"
				"Äther Hydras have [{minion_health}_HP:minion_health], and have [100_äthereal:äthereal] resist.\n"
				"Äther Hydras have a breath weapon which deals [{breath_damage}_äthereal:äthereal] damage.\n"
				"Äther Hydras have a melee attack which deals [{minion_damage}_physical:physical] damage.").format(**self.fmt_dict())
	
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
		if evt.unit == self.owner:
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

class EtherBeam(Level.Spell):
	def __init__(self, elemental):
		Level.Spell.__init__(self)

		self.name = "Äther Beam"
		self.damage = 7
		self.beam = True
		self.cool_down = 7
		self.dtypes = [Ethereal]
		if elemental:
			self.dtypes.append(random.choice([Tags.Fire,Tags.Ice,Tags.Lightning]))

	def get_description(self):
		return "Shoots an Äther Beam"

	def cast(self, x, y):

		start = Point(self.caster.x, self.caster.y)
		target = Point(x, y)

		for point in Bolt(self.caster.level, start, target, find_clear=True):
			self.hit(point.x, point.y, self.dtypes)
		yield

	def get_impacted_tiles(self, x, y):
		tiles = set()
		tiles.add(Point(x, y))

		target = Point(x, y)

		if self.beam:
			for p in Bolt(self.caster.level, self.caster, target):
				tiles.add(p)

		return tiles				

	def hit(self, x, y, dtypes):
		unit = self.caster.level.get_unit_at(x, y)
		if not unit or are_hostile(self.caster, unit):
			for dtype in dtypes:
				self.caster.level.deal_damage(x, y, self.get_stat('damage'), dtype, self)

#Spell summon herd of wyverns that deal little dmg but etherealies enemies
#ethereal storm ethereal extra damage type when etheral choose between lightning
#etherealness aoe ressist change lvl 2 high uses upgrades: shield teleport enemies away
#unit ethereal spider target give enemy buff reappier in x turns deal dmg/ tile hazard reappier in x turns if ocupied nearby(deal dmg)
#enemy frog which etherealness debuff on attack

Spells.all_player_spell_constructors.append(EtherBolt)
Spells.all_player_spell_constructors.append(SummonEtherHydraSpell)
#Upgrades.skill_constructors.append(SpiritShaman)
#Monsters.spawn_options.append((SpriteCloud, 2))
#Variants.variants[Monsters.HellHound].append((((SpiritHound, 2, 4, Variants.WEIGHT_COMMON))))
#RareMonsters.rare_monsters.append((YukiOnna, RareMonsters.DIFF_EASY, 1, 2, Tags.Ice))