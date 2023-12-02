from Level import *
from mods.API_TileHazards.API_TileHazards import TileHazardBasic
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.brimstone import Brimstone
from mods.EtherealPack.models.hazards.util import add_unit, deal_damage
from mods.EtherealPack.tags.Ethereal import Ethereal


class HellStasis(TileHazardBasic):
    def __init__(self, user, source, duration, damage, unit, brimstone, explode, unit_buffs=None):
        TileHazardBasic.__init__(self, "Hell Portal", duration, user)
        self.damage = damage
        self.source = source
        self.unit = unit
        self.unit_buffs = unit_buffs
        self.brimstone = brimstone
        self.explode = explode
        self.asset = ["EtherealPack", "Hell_Stasis"]
        self.gigantism = False
        self.player = [u for u in self.owner.level.units if u.is_player_controlled][0]
        for skill in self.player.get_skills():
            if skill.name == "Äther Gigantism":
                self.gigantism = True

    def get_description(self):
        return ("%s in Stasis takes %d [fire:fire] damage every turn\n%d turns remaining\n"
                "Enemies standing on top take the same damage and get [Ätherealiesed:äthereal] for 2 turns" % (self.unit.name, self.damage, self.duration))

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
                self.user.level.deal_damage(self.x,self.y,self.damage, Tags.Fire, self.source)
            steppy.apply_buff(EtherealnessBuff(), 2)
        killed = deal_damage(self.user.level, self.unit, self.damage, Tags.Fire, self.source)
        
        targets = [u for u in self.user.level.get_units_in_ball(self.unit, 5) if u != self.user and u != self.unit and are_hostile(self.user, u) and u.cur_hp>0]
        if not len(targets) == 0:
            target = random.choice(targets)
            targets.remove(target)
            self.user.level.deal_damage(target.x,target.y,self.damage, Ethereal, self.source)
            self.user.level.deal_damage(target.x,target.y,self.damage, Tags.Fire, self.source)
            if self.brimstone and self.user.level.tiles[target.x][target.y].prop == None:
                self.user.level.add_obj(Brimstone(self.user,self.source,3,self.damage), target.x, target.y)
            if not len(targets) == 0:
                target = random.choice(targets)
                targets.remove(target)
                self.user.level.deal_damage(target.x,target.y,self.damage, Ethereal, self.source)
                self.user.level.deal_damage(target.x,target.y,self.damage, Tags.Fire, self.source)
                if self.brimstone and self.user.level.tiles[target.x][target.y].prop == None:
                    self.user.level.add_obj(Brimstone(self.user,self.source,3,self.damage), target.x, target.y)
                if not len(targets) == 0:
                    target = random.choice(targets)
                    self.user.level.deal_damage(target.x,target.y,self.damage, Ethereal, self.source)
                    self.user.level.deal_damage(target.x,target.y,self.damage, Tags.Fire, self.source)
                    if self.brimstone and self.user.level.tiles[target.x][target.y].prop == None:
                        self.user.level.add_obj(Brimstone(self.user,self.source,3,self.damage), target.x, target.y)
        if killed or self.unit.cur_hp <= 0:
            self.duration = 1
        if self.explode and self.duration == 1:
            radius = round(self.unit.max_hp/8) if self.unit.max_hp <33 else 2 + round(self.unit.max_hp/16)
            for stage in Burst(self.user.level, Point(self.x, self.y), min(math.floor(radius),10)):
                for p in stage:
                    self.user.level.deal_damage(p.x,p.y,self.unit.max_hp/4, Ethereal, self.source)
                    self.user.level.deal_damage(p.x,p.y,self.unit.max_hp/4, Tags.Fire, self.source)
        if self.duration <= 1 and not self.unit.cur_hp <= 0:
            blocking_unit = self.user.level.get_unit_at(self.x,self.y)
            if not blocking_unit:
                add_unit(self.user.level,self.unit, self.x, self.y, self.unit_buffs)
                self.user.level.show_effect(self.x, self.y, Tags.Conjuration)
                if self.unit.gets_clarity:
                    self.unit.apply_buff(StunImmune(),2)
            else:
                p = self.user.level.get_summon_point(self.x, self.y, 20)
                if p:
                    add_unit(self.user.level,self.unit, p.x, p.y, self.unit_buffs)
                    self.user.level.show_effect(p.x, p.y, Tags.Conjuration)
                    if self.unit.gets_clarity:
                        self.unit.apply_buff(StunImmune(),2)
