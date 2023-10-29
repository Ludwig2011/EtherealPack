from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherLinkBuff(Buff):
    def __init__(self, range):
        Buff.__init__(self)
        self.name = "Äther Linked"
        self.buff_type = BUFF_TYPE_BLESS
        self.stack_type	= STACK_NONE
        self.color = Ethereal.color
        self.range = range
        self.old_range = 4
        self.ether_wave = None
        self.owner
        
    def on_applied(self, owner):
        self.ether_wave = [spell for spell in owner.spells if spell.name == "Äther Wave"][0]
        self.ether_wave.cool_down = 2
        self.old_range = self.ether_wave.radius
        self.ether_wave.radius = self.ether_wave.radius + 3
        self.owner = owner
        
    def on_advance(self):
        allies = [u for u in self.owner.level.get_units_in_ball(self.owner, self.range) if u != self.owner and not are_hostile(self.owner, u) and u.name == "Äther Wyvern"]
        if allies:
            self.turns_left = 3
        return super().on_advance()

    def on_unapplied(self):
        self.ether_wave.cool_down = 3
        self.ether_wave.radius = self.old_range