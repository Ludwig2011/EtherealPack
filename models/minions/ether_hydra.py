from CommonContent import SimpleMeleeAttack
from Level import *
from mods.EtherealPack.EtherealPack import Ethereal
from mods.EtherealPack.models.minions.ether_breath import EtherBreath 

def EtherHydra(elemental=False):
	unit = Unit()
	unit.sprite.char = 'D'
	unit.sprite.color = Color(1,121,111)
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