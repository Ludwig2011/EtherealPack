from Level import *
import Spells
import Upgrades
import mods.API_Universal.Modred as Modred
from mods.EtherealPack.models.skills.collect_dispersion import CollectDispersion
from mods.EtherealPack.models.skills.etherpredators import Etherpredators
from mods.EtherealPack.models.skills.ethertuned import Ethertuned
from mods.EtherealPack.models.spells.domain_expansion import DomainExpansion
from mods.EtherealPack.models.spells.ether_bolt import EtherBolt
from mods.EtherealPack.models.spells.ether_eye import EyeOfEtherSpell
from mods.EtherealPack.models.spells.ether_stream import EtherStream
from mods.EtherealPack.models.spells.expanding_force import ExpandingForceSpell
from mods.EtherealPack.models.spells.frost_spire import SummonFrostSpire
from mods.EtherealPack.models.spells.hex import Hex
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

#demons undead dark holy weak, arcane strong (living/nature aswell?)
Tags.elements.append(Ethereal)
Modred.add_tag_keybind(Ethereal, 'Ä')

#Overwrite Level set_default_resistances. Resists API?
Modred.add_tag_tooltip(Ethereal)
Modred.add_tag_tooltip(Etherealness)

# Add custom spells
Modred.add_tag_effect_simple(Ethereal, os.path.join('mods','EtherealPack', 'ether'))

Modred.add_shrine_option(Ethereal, 1)




#Spell summon herd of wyverns that deal little dmg but etherealies enemies
#ethereal storm ethereal extra damage type when etheral choose between lightning
#etherealness aoe ressist change lvl 2 high uses upgrades: shield teleport enemies away
#unit ethereal spider target give enemy buff reappier in x turns deal dmg/ tile hazard reappier in x turns if ocupied nearby(deal dmg)
#enemy frog which etherealness debuff on attack

Spells.all_player_spell_constructors.append(EtherBolt)
Spells.all_player_spell_constructors.append(SummonEtherHydraSpell)
Spells.all_player_spell_constructors.append(Hex)
Spells.all_player_spell_constructors.append(WordOfDisjunction)
Spells.all_player_spell_constructors.append(PyreOfWyvernsSpell)
Spells.all_player_spell_constructors.append(MomentInHell)
Spells.all_player_spell_constructors.append(PureEtherSphere)
Spells.all_player_spell_constructors.append(EtherStormSpell)
Spells.all_player_spell_constructors.append(SummonFrostSpire)
Spells.all_player_spell_constructors.append(Railgun)
Spells.all_player_spell_constructors.append(EtherStream)
Spells.all_player_spell_constructors.append(ExpandingForceSpell)
Spells.all_player_spell_constructors.append(EyeOfEtherSpell)
Spells.all_player_spell_constructors.append(MomentOfBliss)
Spells.all_player_spell_constructors.append(PiercingGaze)
Spells.all_player_spell_constructors.append(DomainExpansion)
Upgrades.skill_constructors.append(Etherpredators)
Upgrades.skill_constructors.append(CollectDispersion)
Upgrades.skill_constructors.append(Ethertuned)
#Monsters.spawn_options.append((SpriteCloud, 2))
#Variants.variants[Monsters.HellHound].append((((SpiritHound, 2, 4, Variants.WEIGHT_COMMON))))
#RareMonsters.rare_monsters.append((YukiOnna, RareMonsters.DIFF_EASY, 1, 2, Tags.Ice))