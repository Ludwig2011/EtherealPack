
# Consitent naming scheme required
from CommonContent import RegenBuff
from Level import *
from mods.EtherealPack.models.buffs.lost_heads_buff import LostHeadsBuff
from mods.EtherealPack.models.minions.ether_hydra import EtherHydra
from mods.EtherealPack.models.spells.ether_bolt import EtherBolt
from mods.EtherealPack.tags.Ethereal import Ethereal


class SummonEtherHydraSpell(Spell):

	def on_init(self):
		self.name = "Äther Hydra"
		self.range = 4
		self.max_charges = 3
		self.asset = ['EtherealPack', 'summon_ether_hydra']
		self.tags = [Ethereal, Tags.Conjuration, Tags.Dragon]
		self.level = 4

		self.minion_health = 45
		self.minion_damage = 9
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
			drake.buffs.append(LostHeadsBuff(self.get_stat('element_mother'),self.get_stat('breath_damage')))

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
				"Äther Hydras have [{minion_health}_HP:minion_health] and [100_äthereal:äthereal], [25_physical:physical] and [-50_arcane:arcane] resist.\n"
				"Äther Hydras have a breath weapon which deals [{breath_damage}_äthereal:äthereal] damage.\n"
				"Äther Hydras have a melee attack which deals [{minion_damage}_physical:physical] damage.\n"
				"Äther Hydras trample over allies to get where they want").format(**self.fmt_dict())
