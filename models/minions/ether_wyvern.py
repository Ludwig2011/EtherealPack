from CommonContent import SimpleMeleeAttack, SimpleBurst, TeleportyBuff
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal 
from mods.EtherealPack.models.minions.ether_wave import EtherWave

def EtherWyvern(shields=2):
	unit = Unit()
	unit.name = "Äther Wyvern"
	unit.description = "Lets out ether waves"
	unit.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
	unit.max_hp = 10
	unit.spells.append(SimpleMeleeAttack(3))
	unit.spells.append(EtherWave())
	unit.shields = shields
	unit.resists[Ethereal] = 50
	unit.resists[Tags.Poison] = 50
	unit.resists[Tags.Physical] = 25
	unit.resists[Tags.Arcane] = -25
	unit.tags = [Tags.Dragon, Tags.Living, Ethereal]
	unit.flying = True
	unit.buffs.append(TeleportyBuff())




	return unit

