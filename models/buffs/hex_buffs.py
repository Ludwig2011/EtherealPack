from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

#watch out that not all buffs check for damage event (check self? or give caster permanent positive buff that checks event)
def HexBuff(Buff):
    def __init__(self,duration,damage,radius):
        Buff.__init__(self)
        self.name = "Hexer"
        self.buff_type = BUFF_TYPE_BLESS
        self.stack_type	= STACK_NONE
        self.duration = duration
        self.damage = damage
        self.radius = radius
        self.global_triggers[EventOnDamaged] = self.on_damaged

    def on_damage(self,evt):
        if evt.unit and evt.unit.has_buff(HexDebuff):
            self.owner.level.deal_damage(evt.unit.x,evt.unit.y, self.get_stat('damage'), Tags.Dark, self)
            self.owner.level.deal_damage(evt.unit.x,evt.unit.y, self.get_stat('damage'), Ethereal, self)

# just a marker
def HexDebuff(Buff):
    def __init__(self):
        Buff.__init__(self)
        self.buff_type = BUFF_TYPE_CURSE
        self.stack_type	= STACK_REPLACE
        self.name = "Hex"
        self.color = Ethereal.color
