import random

from Level import Component, Tags
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherealComponent(Component):

    def on_pickup(self, player, level):
        spells = [
            spell for spell in player.spells
            if Ethereal in spell.tags and spell.cur_charges < spell.get_stat('max_charges')
        ]
        if spells:
            random.choice(spells).refund_charges(100)
            level.show_effect(player.x, player.y, Ethereal)


class EtherealDust(EtherealComponent):

    def on_init(self):
        self.name = "Ethereal Dust"
        self.asset = ["EtherealPack", "ether"]
        self.description = "On Pickup: Restore 100 charge to a random Ethereal spell."
        self.tags = [Ethereal]


class EtherealLens(EtherealComponent):
#TODO ether debuff all enemies
    def on_init(self):
        self.name = "Ethereal Lens"
        self.asset = ["EtherealPack", "beholding_eyes"]
        self.description = "On Pickup: Restore 100 charge to a random Ethereal spell."
        self.tags = [Ethereal, Tags.Eye]


class EtherealBloom(EtherealComponent):
#TODO summon spuders
    def on_init(self):
        self.name = "Ethereal Bloom"
        self.asset = ["EtherealPack", "ether_lord"]
        self.description = "On Pickup: Restore 100 charge to a random Ethereal spell."
        self.tags = [Ethereal, Tags.Nature]


class EtherealFrost(EtherealComponent):
#TODO reduce resistances in line of sight
    def on_init(self):
        self.name = "Ethereal Frost"
        self.asset = ["EtherealPack", "pure_ether"]
        self.description = "On Pickup: Restore 100 charge to a random Ethereal spell."
        self.tags = [Ethereal, Tags.Ice]