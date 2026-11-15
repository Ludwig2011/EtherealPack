from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.brimstone import Brimstone
from mods.EtherealPack.models.hazards.stasis import TranslocationStasis
from mods.EtherealPack.models.hazards.util import deal_off_grid_damage
from mods.EtherealPack.tags.Ethereal import Ethereal


class HellStasis(TranslocationStasis):
    def __init__(self, user, source, duration, damage, unit, brimstone, explode, unit_buffs=None):
        TranslocationStasis.__init__(
            self,
            "Hell Portal",
            ["EtherealPack", "Hell_Stasis"],
            user,
            source,
            duration,
            unit,
            unit_buffs,
        )
        self.damage = damage
        self.brimstone = brimstone
        self.explode = explode

    def get_description(self):
        unit_name = self.unit.name if self.unit is not None else "Empty Hell Portal"
        return ("%s in Stasis takes %d [fire:fire] damage every turn\n%d turns remaining\n"
                "Enemies standing on top take the same damage and get [Ätherealiesed:äthereal] for 2 turns" % (unit_name, self.damage, self.duration))

    def advance_effect(self):
        self.apply_gigantism()

        steppy = self.user.level.get_unit_at(self.x,self.y)
        if steppy: 
            if are_hostile(self.user, steppy):
                self.user.level.deal_damage(self.x,self.y,self.damage, Tags.Fire, self.source)
            steppy.apply_buff(EtherealnessBuff(), 2)

        killed = False
        if self.unit is not None:
            killed = deal_off_grid_damage(
                self.user.level, self.unit, self.damage, Tags.Fire, self.source
            )
        center = self.unit if self.unit is not None else Point(self.x, self.y)
        targets = [
            u
            for u in self.user.level.get_units_in_ball(center, 5)
            if u != self.user
            and u is not self.unit
            and are_hostile(self.user, u)
            and u.cur_hp > 0
        ]
        for _ in range(3):
            if not targets:
                break
            target = random.choice(targets)
            targets.remove(target)
            self.user.level.deal_damage(target.x,target.y,self.damage, Ethereal, self.source)
            self.user.level.deal_damage(target.x,target.y,self.damage, Tags.Fire, self.source)
            tile = self.user.level.tiles[target.x][target.y]
            if self.brimstone and not getattr(tile, "hazards", None):
                self.user.level.add_hazard(
                    Brimstone(self.user, self.source, 3, self.damage),
                    target.x,
                    target.y,
                )
        if self.unit is not None:
            if killed or self.unit.cur_hp <= 0:
                self.duration = 1
            if self.explode and self.duration == 1:
                radius = (
                    round(self.unit.max_hp / 8)
                    if self.unit.max_hp < 33
                    else 2 + round(self.unit.max_hp / 16)
                )
                for stage in Burst(
                    self.user.level, Point(self.x, self.y), min(math.floor(radius), 10)
                ):
                    for p in stage:
                        self.user.level.deal_damage(
                            p.x, p.y, self.unit.max_hp / 4, Ethereal, self.source
                        )
                        self.user.level.deal_damage(
                            p.x, p.y, self.unit.max_hp / 4, Tags.Fire, self.source
                        )
        self.return_unit()
