from Level import *
import Spells
import mods.API_Universal.Modred as Modred
from mods.EtherealPack.models.spells.ether_bolt import EtherBolt
from mods.EtherealPack.models.spells.summon_ether_hydra import SummonEtherHydraSpell
from mods.EtherealPack.tags.Ethereal import Ethereal, Etherealness
from mods.EtherealPack.models.spells.pyre_of_wyverns import PyreOfWyvernsSpell

#demons undead dark holy weak, arcane strong (living/nature aswell?)
Tags.elements.append(Ethereal)
Modred.add_tag_keybind(Ethereal, 'Ä')


Modred.add_tag_tooltip(Ethereal)
Modred.add_tag_tooltip(Etherealness)

# Add custom spells
#Modred.add_tag_effect_simple(Tags.Ethereal, os.path.join('mods','EtherealPack', ''))

Modred.add_shrine_option(Ethereal, 1)




#Spell summon herd of wyverns that deal little dmg but etherealies enemies
#ethereal storm ethereal extra damage type when etheral choose between lightning
#etherealness aoe ressist change lvl 2 high uses upgrades: shield teleport enemies away
#unit ethereal spider target give enemy buff reappier in x turns deal dmg/ tile hazard reappier in x turns if ocupied nearby(deal dmg)
#enemy frog which etherealness debuff on attack

Spells.all_player_spell_constructors.append(EtherBolt)
Spells.all_player_spell_constructors.append(SummonEtherHydraSpell)
Spells.all_player_spell_constructors.append(PyreOfWyvernsSpell)
#Upgrades.skill_constructors.append(SpiritShaman)
#Monsters.spawn_options.append((SpriteCloud, 2))
#Variants.variants[Monsters.HellHound].append((((SpiritHound, 2, 4, Variants.WEIGHT_COMMON))))
#RareMonsters.rare_monsters.append((YukiOnna, RareMonsters.DIFF_EASY, 1, 2, Tags.Ice))