from CommonContent import SimpleRangedAttack
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.stasis import TranslocationStasis
from mods.EtherealPack.models.hazards.util import deal_off_grid_damage


class BlissStasis(TranslocationStasis):
    def __init__(self, user, source, duration, radius, damage, unit, blind, bless, unit_buffs=None):
        TranslocationStasis.__init__(
            self,
            "Bliss Portal",
            ["EtherealPack", "bliss_stasis"],
            user,
            source,
            duration,
            unit,
            unit_buffs,
        )
        self.damage = damage
        self.radius = radius
        self.blind = blind
        self.bless = bless

    def get_description(self):
        unit_name = self.unit.name if self.unit is not None else "Empty Bliss Portal"
        return ("%s in Stasis heals %d [hp:heal] every turn\n%d turns remaining\n"
                "Allies standing on top heal for the same amount and anyone gets [Ätherealiesed:äthereal] for 2 turns" % (unit_name, self.damage, self.duration))

    def advance_effect(self):
        self.apply_gigantism()

        steppy = self.user.level.get_unit_at(self.x,self.y)
        if steppy: 
            if are_hostile(self.user, steppy):
                self.user.level.deal_damage(self.x,self.y,-self.damage, Tags.Heal, self.source)
            steppy.apply_buff(EtherealnessBuff(), 2)

        killed = False
        if self.unit is not None:
            killed = deal_off_grid_damage(
                self.user.level, self.unit, -self.damage, Tags.Heal, self.source
            )

        targets = [u for u in self.user.level.get_units_in_ball(self.user, self.radius) if u != self.user and u != self.unit and not are_hostile(self.user, u) and u.cur_hp>0]
        for target in targets:
            self.user.level.deal_damage(target.x,target.y,-self.damage, Tags.Heal, self.source)
        if self.blind:
            targets = [u for u in self.user.level.get_units_in_ball(self.user, self.radius) if u != self.user and u != self.unit and are_hostile(self.user, u) and u.cur_hp>0]
            for target in targets:
                target.apply_buff(BlindBuff(), 3)
        if self.unit is not None and (killed or self.unit.cur_hp <= 0):
            self.duration = 1
        self.return_unit()

    def on_unit_returned(self):
        if self.bless:
            self.unit.apply_buff(BlissfullBlessing())

class BlissfullBlessing(Buff):
    def __init__(self):
        Buff.__init__(self)
        self.name = "Blissfull Blessing"
        #self.buff_type = BUFF_TYPE_BLESS
        #self.stack_type	= STACK_NONE
        self.color = Tags.Holy.color
        self.heal = 3
        self.description = "Gains 100 Holy resist, Blissfull Bolt and 3 HP regen"

    def on_applied(self, owner):
        owner.resists[Tags.Holy] +=100
        bliss_bolt = SimpleRangedAttack("Blissfull Bolt",7,Tags.Holy,7,cool_down=3)
        bliss_bolt.caster = owner
        owner.spells.insert(1, bliss_bolt)
        return super().on_applied(owner)
    
    def on_advance(self):
        if self.owner.cur_hp < self.owner.max_hp:
            self.owner.deal_damage(-self.heal, Tags.Heal, self)