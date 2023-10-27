from CommonContent import SimpleMeleeAttack, SimpleBurst, TeleportyBuff
from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal 
from mods.EtherealPack.models.minions.ether_wave import EtherWave

def EtherWyvern(shields=2, elemental=False, ether_link=False):
	unit = Unit()
	unit.name = "Äther Wyvern"
	unit.description = "tbd"
	unit.max_hp = 10
	unit.spells.append(SimpleMeleeAttack(6))
	unit.shields = shields
	unit.resists[Ethereal] = 50
	unit.resists[Tags.Arcane] = -25
	unit.tags = [Tags.Dragon, Tags.Living, Ethereal]
	unit.flying = True
	unit.buffs.append(TeleportyBuff())

	if(ether_link):
		unit.spells.append(EtherWave())
	else:
		burst_spell = SimpleBurst(3, 4, damage_type=Ethereal, cool_down=3, ignore_walls=True, onhit=lambda caster, unit: unit.apply_buff(EtherealnessBuff(), 7))
		burst_spell.friendly_fire = False
		unit.spells.append(burst_spell)




	return unit

