
from Level import *
from mods.EtherealPack.models.buffs.ether_link_buff import EtherLinkBuff


class EtherLink(Spell):
    def __init__(self):
        Spell.__init__(self)

        self.name = "Äther Link"
        self.cool_down = 7
        self.range = 7
        self.can_target_self = True

    def get_description(self):
        return "Link up to wyvern friends"

    def cast_instant(self, x, y):
        self.caster.apply_buff(EtherLinkBuff(self.range), 3)
        
    def get_ai_target(self):
        if self.caster.has_buff(EtherLinkBuff):
            return None
        allies = [u for u in self.caster.level.get_units_in_ball(self.caster, self.range) if u != self.caster and not are_hostile(self.caster, u) and u.name == "Äther Wyvern"]
        if allies:
            return self.caster
        return None
