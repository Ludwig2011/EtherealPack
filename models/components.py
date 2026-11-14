import random

from Level import Component, Tags, are_hostile
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.equipment.etherpredators import EtherSpider
from mods.EtherealPack.tags.Ethereal import Ethereal

class EtherealDust(Component):

    def on_init(self):
        self.name = "Ethereal Dust"
        self.asset = ["EtherealPack", "ether"]
        self.description = "On Pickup: Restore 100 charge to a random Ethereal spell."
        self.tags = [Ethereal]

    def on_pickup(self, player, level):
        spells = [
            spell for spell in player.spells
            if Ethereal in spell.tags and spell.cur_charges < spell.get_stat('max_charges')
        ]
        if spells:
            random.choice(spells).refund_charges(100)
            level.show_effect(player.x, player.y, Ethereal)


class EtherealLens(Component):
    def on_init(self):
        self.name = "Ethereal Lens"
        self.asset = ["EtherealPack", "beholding_eyes"]
        self.description = "On Pickup: Ätherlielise all enemies for 15 turns."
        self.tags = [Ethereal, Tags.Eye]

    def on_pickup(self, player, level):
        for unit in level.units:
            if are_hostile(player, unit):
                unit.apply_buff(EtherealnessBuff(), 15)


class EtherealBloom(Component):
    def on_init(self):
        self.name = "Ethereal Bloom"
        self.asset = ["EtherealPack", "ether_lord"]
        self.description = "On Pickup: Summon 7 Äther Spiders."
        self.tags = [Ethereal, Tags.Nature]

    def on_pickup(self, player, level):
        for i in range(7):
            level.summon(player, EtherSpider(14, 7, 7), radius=36, sort_dist=False)


class EtherealFrost(Component):
    def on_init(self):
        self.name = "Ethereal Frost"
        self.asset = ["EtherealPack", "pure_ether"]
        self.description = "On Pickup: Reduce Ice and Äthereal resistances of all enemies in line of sight by 100%"
        self.tags = [Ethereal, Tags.Ice]

    def on_pickup(self, player, level):
        units = level.get_units_in_los(player)
        for unit in units:
            if are_hostile(player, unit):
                unit.resists[Ethereal] -= 100
                unit.resists[Tags.Ice] -= 100

#TODO rare component that upgrades spell to consume atherealness of enemies to deal extra damage