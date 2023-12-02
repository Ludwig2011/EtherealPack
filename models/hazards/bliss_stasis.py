from CommonContent import SimpleRangedAttack
from Level import *
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.util import add_unit, deal_damage


class BlissStasis(TileHazardBasic):
    def __init__(self, user, source, duration, radius, damage, unit, blind, bless, unit_buffs=None):
        TileHazardBasic.__init__(self, "Bliss Portal", duration, user)
        self.damage = damage
        self.radius = radius
        self.source = source
        self.unit = unit
        self.unit_buffs = unit_buffs
        self.blind = blind
        self.bless = bless
        self.asset = ["EtherealPack", "Hell_Stasis"] # ["EtherealPack", "Bliss_Stasis"]
        self.gigantism = False
        self.player = [u for u in self.owner.level.units if u.is_player_controlled][0]
        for skill in self.player.get_skills():
            if skill.name == "Äther Gigantism":
                self.gigantism = True

    def get_description(self):
        return ("%s in Stasis heals %d [hp:heal] every turn\n%d turns remaining\n"
                "Allies standing on top heal for the same amount and get [Ätherealiesed:äthereal] for 2 turns" % (self.unit.name, self.damage, self.duration))

    def effect(self, unit):
        pass

    def advance_effect(self):
        if self.gigantism and not are_hostile(self.unit, self.user):
            self.unit.max_hp += 5
            for spell in self.unit.spells:
                if hasattr(spell, "damage"):
                    spell.damage += 2
        steppy = self.user.level.get_unit_at(self.x,self.y)
        if steppy: 
            if are_hostile(self.user, steppy):
                self.user.level.deal_damage(self.x,self.y,-self.damage, Tags.Heal, self.source)
            steppy.apply_buff(EtherealnessBuff(), 2)
        killed = deal_damage(self.user.level, self.unit, -self.damage, Tags.Heal, self.source)
        targets = [u for u in self.user.level.get_units_in_ball(self.user, self.radius) if u != self.user and u != self.unit and not are_hostile(self.user, u) and u.cur_hp>0]
        for target in targets:
            self.user.level.deal_damage(target.x,target.y,-self.damage, Tags.Heal, self.source)
        if self.blind:
            targets = [u for u in self.user.level.get_units_in_ball(self.user, self.radius) if u != self.user and u != self.unit and are_hostile(self.user, u) and u.cur_hp>0]
            for target in targets:
                target.apply_buff(BlindBuff(), 3)
        if killed or self.unit.cur_hp <= 0:
            self.duration = 1
        if self.duration <= 1 and not self.unit.cur_hp <= 0:
            blocking_unit = self.user.level.get_unit_at(self.x,self.y)
            if not blocking_unit:
                add_unit(self.user.level,self.unit, self.x, self.y, self.unit_buffs)
                if self.bless:
                    self.unit.apply_buff(BlissfullBlessing())
                self.user.level.show_effect(self.x, self.y, Tags.Conjuration)
                if self.unit.gets_clarity:
                    self.unit.apply_buff(StunImmune(),2)
            else:
                p = self.user.level.get_summon_point(self.x, self.y, 20)
                if p:
                    add_unit(self.user.level,self.unit, p.x, p.y, self.unit_buffs)
                    if self.bless:
                        self.unit.apply_buff(BlissfullBlessing())
                    self.user.level.show_effect(p.x, p.y, Tags.Conjuration)
                    if self.unit.gets_clarity:
                        self.unit.apply_buff(StunImmune(),2)

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