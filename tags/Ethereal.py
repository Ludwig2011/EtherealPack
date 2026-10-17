import ModHandler
from Level import Color, Tag
#TODO fix description color and variables in spells/equipment
#TODO make spells/equipment scale with appropiate spell bonuses where not already done. Mostly missing for upgrades / equipment
#TODO Rename skill folder toequipment and make sure imports etc dont break 
#TODO make the following resistance genericly apply to units:
#Äther strong against Constructs, Undead, Holy and Dark
#Äther units weak to arcane
Ethereal = ModHandler.register_tag("Äthereal", Color(1, 255, 188), letter="v", asset=["EtherealPack", "ether"])
Etherealness = Tag("Ätherealness", Color(1, 255, 188))