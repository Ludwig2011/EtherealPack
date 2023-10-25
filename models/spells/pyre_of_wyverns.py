from Level import *

class PyreOfWyvernsSpell(Spell):

	def on_init(self):

		self.name = "Pyre of Wyverns"

		self.minion_health = 10
		self.minion_damage = 6
		self.minion_range = 5
		self.num_summons = 3
		self.shields = 2

		self.max_charges = 2

		self.upgrades['num_summons'] = (2, 3)
		self.upgrades['shields'] = (2, 4)
		self.upgrades['thunderbirds'] = 1, 4, "Thunderbirds", "Summon thunderbirds instead of eagles.  Thunderbirds deal and resist [lightning] damage."

		self.range = 0

		self.level = 5
		self.tags = [Tags.Conjuration, Tags.Nature, Tags.Holy]

	def get_description(self):
		return ("Summons [{num_summons}_eagles:num_summons] near the caster.\n"
				"Eagles have [{minion_health}_HP:minion_health] and can fly.\n"
				"Eagles have a melee attack which deals [{minion_damage}_physical:physical] damage.").format(**self.fmt_dict())

	def cast_instant(self, x, y):
		for i in range(self.get_stat('num_summons')):
			eagle = Unit()
			eagle.name = "Eagle"

			dive = LeapAttack(damage=self.get_stat('minion_damage'), range=self.get_stat('minion_range'), is_leap=True)
			peck = SimpleMeleeAttack(damage=self.get_stat('minion_damage'))

			dive.name = 'Dive'
			peck.name = 'Claw'

			eagle.spells.append(peck)
			if self.get_stat('dive_attack'):
				eagle.spells.append(dive)
			eagle.max_hp = self.get_stat('minion_health')
			eagle.team = self.caster.team

			eagle.flying = True
			eagle.tags = [Tags.Living, Tags.Holy, Tags.Nature]

			eagle.shields = self.get_stat('shields')

			if self.get_stat('thunderbirds'):
				for s in eagle.spells:
					s.damage_type = Tags.Lightning
				eagle.tags.append(Tags.Lightning)
				eagle.resists[Tags.Lightning] = 100
				eagle.name = "Thunderbird"

			self.summon(eagle, Point(x, y))