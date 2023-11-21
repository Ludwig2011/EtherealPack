from CommonContent import DamageAuraBuff
from Level import *


class ExpandingForceBuff(DamageAuraBuff):

	def __init__(self, spell):
		self.spell = spell
		DamageAuraBuff.__init__(self, damage=self.spell.aura_damage, radius=self.spell.get_stat('radius'), damage_type=[Tags.Arcane, Tags.Dark], friendly_fire=False)

	def get_description(self):
		return "%d damage dealt" % self.damage_dealt



class ExpandingForceSpell(Spell):

	def on_init(self):

		self.range = 0
		self.max_charges = 2
		self.name = "Expanding Force"
		self.aura_damage = 2
		self.radius = 7
		self.duration = 30

		self.stats.append('aura_damage')

		self.upgrades['radius'] = (3, 2)
		self.upgrades['duration'] = 15
		self.upgrades['max_charges'] = (4, 2)

		self.upgrades['teleport_blocker'] = (1, 5, "Teleport Blocker", "When an enemy teleports inside this .")
		
		self.tags = [Tags.Enchantment, Tags.Dark, Tags.Arcane]
		self.level = 3

	def cast_instant(self, x, y):
		buff = ExpandingForceBuff(self)
		buff.stack_type = STACK_REPLACE
		buff.color = Tags.Arcane.color
		buff.name = "Nightmare Aura"
		buff.source = self
		self.caster.apply_buff(buff, self.get_stat('duration'))

	def get_description(self):
		return ("Each turn, randomly deals [{aura_damage}_arcane:arcane] or [{aura_damage}_dark:dark] damage to each enemy in a [{radius}_tile:radius] radius.\n"
				"This damage is fixed, and cannot be increased using shrines, skills, or buffs.\n"
				"Lasts [{duration}_turns:duration].").format(**self.fmt_dict())