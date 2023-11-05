#charge railgun cast -> gain charge buff every turn and change name to fire railgun
#fire railgun cast -> change name back and has range and damage based on turns charged(buff duration goes up instead of down?) and gets rid of buff
# max pool of damage that gets reduced per unit hit? to a max per unit?
# damage in straight line, ?destroy walls based on charge or upgrade?
# charge speed upgrade

from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal

class Railgun(Spell):
    def on_init(self):
        self.name = "Charge Railgun"
        self.tags = [Tags.Sorcery, Tags.Metallic, Ethereal]
        self.level = 2

        self.damage_types = [Ethereal, Tags.Physical]

        self.max_charges = 7
        self.max_damage = 50
        self.range = 0 
        self.damage = 0 
        self.radius = 1
        self.charge_speed = 4
        self.requires_los = True

        self.upgrades['charge_speed'] = (3, 2)
        self.upgrades['max_damage'] = (50, 2)
        self.upgrades['max_charges'] = (7, 2)
        self.upgrades['radius'] = (1, 2)
        self.upgrades['requires_los'] = (-1, 2, "Wall Buster", "Destroy walls in the center path".format(**self.fmt_dict()))
        

    def cast(self, x, y):
        if self.name == "Fire Railgun":
            center_beam = self.caster.level.get_points_in_line(self.caster, Point(x, y), find_clear=True)[1:]
            side_beam = []
            side_beam_damage = []
            for p in center_beam:
                unit = self.caster.level.get_unit_at(p.x,p.y)
                self.caster.level.deal_damage(p.x, p.y, self.get_stat('damage'), Tags.Physical, self)
                self.caster.level.deal_damage(p.x, p.y, self.get_stat('damage')/2, Ethereal, self)
                if not self.caster.level.tiles[p.x][p.y].can_see:
                    self.caster.level.make_floor(p.x, p.y)
                if unit:
                    self.damage -= 5
                    if self.damage < 0:
                        self.damage = 0
                for q in self.caster.level.get_points_in_ball(p.x, p.y, self.get_stat('radius')+0.5):
                    if q.x == self.caster.x and q.y == self.caster.y:
                        continue
                    if q not in center_beam and q not in side_beam:
                        side_beam.append(q)
                        side_beam_damage.append(self.damage)

            for i, p in enumerate(side_beam):
                self.caster.level.deal_damage(p.x, p.y, side_beam_damage[i]/2, Ethereal, self)
            for buff in self.caster.buffs:
                if isinstance(buff, RailgunBuff):
                    self.caster.remove_buff(buff)
            self.name = "Charge Railgun"
            yield
        else:
            self.caster.apply_buff(RailgunBuff(self.get_stat('charge_speed'),self.get_stat('max_damage'),self),1)
            self.cur_charges += 1
            self.name = "Fire Railgun"

    def get_impacted_tiles(self, x, y):
        center_beam = self.caster.level.get_points_in_line(self.caster, Point(x, y), find_clear=True)[1:]
        side_beam = []
        for p in center_beam:
            for q in self.caster.level.get_points_in_ball(p.x, p.y, self.get_stat('radius')+0.5):
                if q.x == self.caster.x and q.y == self.caster.y:
                    continue
                if q not in center_beam and q not in side_beam:
                    side_beam.append(q)
        return center_beam + side_beam
        
    def get_description(self):
        return ("Trap a coin between two rifts steadily increasing its momentum\n" 
                "Then shoot the coin across a line that deals [physical:physical] damage to all units [hit:damage] and half [äthereal:äthereal] damage to all units in and surounding the line aswell.\n"
                "Cast once to start charging. Recast to fire. Gains %d range and %d damage for every turn charged (at most %d). Loses 5 damage for every target [hit:damage]"
                % (math.floor(self.get_stat('charge_speed')/3), self.get_stat('charge_speed'), self.get_stat('max_damage'))).format(**self.fmt_dict())

class RailgunBuff(Buff):
    def __init__(self,charge_speed, max_damage, railgun):
        Buff.__init__(self)
        self.name = "Charging Railgun"
        self.buff_type = BUFF_TYPE_BLESS
        self.stack_type	= STACK_REPLACE
        self.charge_speed = charge_speed
        self.max_damage = max_damage
        self.railgun = railgun
        
    def advance(self):
        if self.applied:
            if self.turns_left > 0:
                self.turns_left += 1
                self.railgun.damage += self.charge_speed
                if self.railgun.damage > self.max_damage:
                    self.railgun.damage = self.max_damage
                self.railgun.range += math.floor(self.charge_speed/3)
            else:
                self.owner.remove_buff(self)

    def on_unapplied(self):
        self.railgun.damage = 0
        self.railgun.range = 0
        return super().on_unapplied()
    