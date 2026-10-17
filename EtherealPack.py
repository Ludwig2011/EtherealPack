import Spells
import Equipment as EquipmentContent
import ModHandler
from mods.EtherealPack.models.components import EtherealDust, EtherealLens, EtherealBloom, EtherealFrost
from mods.EtherealPack.models.skills.beholding_eyes import BeholdingEyes
from mods.EtherealPack.models.skills.collect_dispersion import CollectDispersion
from mods.EtherealPack.models.skills.ether_gigantism import EtherGigantism
from mods.EtherealPack.models.skills.ether_lord import EtherLord
from mods.EtherealPack.models.skills.etherpredators import Etherpredators
from mods.EtherealPack.models.skills.ethertuned import Ethertuned
from mods.EtherealPack.models.skills.vastness import Vastness
from mods.EtherealPack.models.spells.domain_expansion import DomainExpansion
from mods.EtherealPack.models.spells.ether_bolt import EtherBolt
from mods.EtherealPack.models.spells.ether_eye import EyeOfEtherSpell
from mods.EtherealPack.models.spells.ether_stream import EtherStream
from mods.EtherealPack.models.spells.ethernity import Ethernity
from mods.EtherealPack.models.spells.expanding_force import ExpandingForceSpell
from mods.EtherealPack.models.spells.frost_spire import SummonFrostSpire
from mods.EtherealPack.models.spells.hex import Hex
from mods.EtherealPack.models.spells.mass_stasis import MassStasis
from mods.EtherealPack.models.spells.moment_in_hell import MomentInHell
from mods.EtherealPack.models.spells.moment_of_bliss import MomentOfBliss
from mods.EtherealPack.models.spells.piercing_gaze import PiercingGaze
from mods.EtherealPack.models.spells.pure_ether_sphere import PureEtherSphere
from mods.EtherealPack.models.spells.railgun import Railgun
from mods.EtherealPack.models.spells.summon_ether_hydra import SummonEtherHydraSpell
from mods.EtherealPack.models.spells.word_of_disjunction import WordOfDisjunction
from mods.EtherealPack.tags.Ethereal import Ethereal, Etherealness
from mods.EtherealPack.models.spells.pyre_of_wyverns import PyreOfWyvernsSpell
from mods.EtherealPack.models.spells.ether_storm import EtherStormSpell

#enemy frog which etherealness debuff on attack

Spells.all_player_spell_constructors.extend([
	EtherBolt,
	SummonEtherHydraSpell,
	Hex,
	WordOfDisjunction,
	PyreOfWyvernsSpell,
	MomentInHell,
	PureEtherSphere,
	EtherStormSpell,
	SummonFrostSpire,
	Railgun,
	EtherStream,
	ExpandingForceSpell,
	EyeOfEtherSpell,
	MomentOfBliss,
	PiercingGaze,
	DomainExpansion,
	Ethernity,
	MassStasis,
])

EquipmentContent.all_equipment.extend([
	BeholdingEyes,
	CollectDispersion,
	EtherGigantism,
	EtherLord,
	Etherpredators,
	Ethertuned,
	Vastness,
])

for component in [EtherealDust, EtherealLens, EtherealBloom, EtherealFrost]:
	ModHandler.register_component(component)
#Monsters.spawn_options.append((SpriteCloud, 2))
#Variants.variants[Monsters.HellHound].append((((SpiritHound, 2, 4, Variants.WEIGHT_COMMON))))
#RareMonsters.rare_monsters.append((YukiOnna, RareMonsters.DIFF_EASY, 1, 2, Tags.Ice))