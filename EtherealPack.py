import os
from random import random
import Spells
from CommonContent import RegenBuff, SimpleMeleeAttack
import Level, Upgrades
from Level import Bolt, Color, EventOnDamaged, Point, Tags, are_hostile
import mods.API_Universal.Modred as Modred
import EtherBolt

Ethereal = Level.Tag("Äthereal", Level.Color(1,121,111))
#demons undead dark holy weak, arcane strong (living/nature aswell?)
Level.Tags.elements.append(Ethereal)
Modred.add_tag_keybind(Ethereal, 'Ä')

Etherealness = Level.Tag("Ätherealness", Level.Color(1,121,111))

Modred.add_tag_tooltip(Ethereal)
Modred.add_tag_tooltip(Etherealness)

# Add custom spells
#Modred.add_tag_effect_simple(Level.Tags.Ethereal, os.path.join('mods','EtherealPack', ''))

Modred.add_shrine_option(Ethereal, 1)

#SPELLS



#Spell summon herd of wyverns that deal little dmg but etherealies enemies
#ethereal buff for chain effects
#ethereal storm more bolts when etheral
#etherealness aoe ressist change lvl 2 high uses upgrades: shield teleport enemies away
#unit ethereal spider target give enemy buff reappier in x turns deal dmg/ tile hazard reappier in x turns if ocupied nearby(deal dmg)
#enemy frog which etherealness debuff on attack

Spells.all_player_spell_constructors.append(EtherBolt)
Spells.all_player_spell_constructors.append(SummonEtherHydraSpell)
#Upgrades.skill_constructors.append(SpiritShaman)
#Monsters.spawn_options.append((SpriteCloud, 2))
#Variants.variants[Monsters.HellHound].append((((SpiritHound, 2, 4, Variants.WEIGHT_COMMON))))
#RareMonsters.rare_monsters.append((YukiOnna, RareMonsters.DIFF_EASY, 1, 2, Level.Tags.Ice))