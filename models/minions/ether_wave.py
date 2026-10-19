from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal 
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff

class EtherWave(Spell):

    def __init__(self, minion_damage=3, minion_range=4, shielding_waves=False, ether_link=False):
        Spell.__init__(self)
        self.damage = minion_damage
        self.damage_type = Ethereal
        self.name = "Äther Wave"
        self.cool_down = 3
        self.radius = minion_range
        self.shielding_waves = shielding_waves
        self.ether_link = ether_link
        self.friendly_fire = False
        self.ignore_walls = True


    def on_init(self):
        self.range = 0
        
    def get_ai_target(self):
        for p in self.get_impacted_tiles(self.caster.x, self.caster.y):
            u = self.caster.level.get_unit_at(p.x, p.y)
            if self.shielding_waves and u:
                return self.caster
            elif u and are_hostile(u, self.caster):
                return self.caster

        return None

    def get_description(self):
        desc = "Deals damage in a burst around the caster."
        if self.ignore_walls:
            desc += "\nThe burst ignores walls."
        return desc

    def get_impacted_tiles(self, x, y):
        radius = self.get_stat('radius')
        if self.has_ether_wyvern_nearby(x, y):
            radius += 3
        for stage in Burst(self.caster.level, Point(x, y), radius, ignore_walls=self.ignore_walls):
            for p in stage:
                yield p

    def can_threaten(self, x, y):
        if distance(self.caster, Point(x, y)) > self.radius:
            return False

        # Potential optimization- only make the aoe once per frame
        return Point(x, y) in list(self.get_impacted_tiles(self.caster.x, self.caster.y))

    def cast_instant(self, x, y):
        if self.has_ether_wyvern_nearby(x, y):
            self.cool_down = 2
        else:
            self.cool_down = 3

        for p in self.get_impacted_tiles(x, y):
            unit = self.caster.level.get_unit_at(p.x, p.y)
            if unit:
                if are_hostile(self.caster, unit):
                    self.caster.level.deal_damage(
                        p.x, p.y, self.damage, self.damage_type, self
                    )
                elif self.shielding_waves:
                    unit.shields += 1 if unit.shields <= 1 else 0

                if unit.cur_hp > 0:
                    unit.apply_buff(EtherealnessBuff(), 3)

            if random.random() < 0.3:
                self.caster.level.show_effect(p.x, p.y, Ethereal)

    def has_ether_wyvern_nearby(self, x, y):
        from mods.EtherealPack.models.minions.ether_wave import EtherWyvern
        return self.ether_link and any(
            isinstance(unit, EtherWyvern)
            for unit in self.caster.level.get_units_in_ball(Point(x, y), 7)
        )