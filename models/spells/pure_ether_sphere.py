import random

from Level import *
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.tags.Ethereal import Ethereal
from Spells import Orb


class PureEtherSphereBuff(Buff):
    def __init__(self, spell, destination=None):
        self.spell = spell
        self.destination = destination
        self.discharge_cooldown = 0
        Buff.__init__(self)

    def on_init(self):
        self.name = "Pure Ether Sphere"
        self.color = Ethereal.color

    def on_advance(self):
        orb = self.owner
        level = orb.level
        spell = self.spell
        radius = spell.get_stat("radius")
        duration = spell.get_stat("duration")
        damage = spell.get_stat("minion_damage")

        if self.destination is None:
            return

        path = level.get_points_in_line(orb, self.destination)[1:]
        next_point = path[0] if path else None
        if next_point is not None:
            if spell.get_stat("melt_walls") and level.tiles[
                next_point.x
            ][next_point.y].is_wall():
                level.make_floor(next_point.x, next_point.y)
            if level.can_move(orb, next_point.x, next_point.y, teleport=True):
                level.act_move(orb, next_point.x, next_point.y, teleport=True)

        if spell.get_stat("pure_discharge"):
            if self.discharge_cooldown <= 0:
                targets = [
                    unit
                    for unit in level.get_units_in_los(orb)
                    if unit != orb and are_hostile(orb, unit) and unit.is_alive()
                ]
                for target in random.sample(targets, min(3, len(targets))):
                    self.zap(target)
                self.discharge_cooldown = 2
            else:
                self.discharge_cooldown -= 1

        self.spread_ether(orb.x, orb.y, radius, duration, damage)
        if next_point is None:
            orb.kill()

    def zap(self, target):
        spell = self.spell
        level = self.owner.level
        target.apply_buff(Stun(), 2)
        self.spread_ether(
            target.x,
            target.y,
            spell.get_stat("radius"),
            spell.get_stat("duration"),
            spell.get_stat("minion_damage"),
        )
        for point in level.get_points_in_line(self.owner, target, find_clear=True)[
            1:-1
        ]:
            level.show_effect(point.x, point.y, Ethereal, minor=True)

    def spread_ether(self, x, y, radius, duration, damage):
        level = self.owner.level
        # Keep the original eight-neighbor spread at base radius.
        use_diagonal_distance = radius <= 1
        for point in level.get_points_in_ball(
            x, y, radius, diag=use_diagonal_distance
        ):
            if level.tiles[point.x][point.y].prop is not None:
                continue
            hazard = PureEther(
                self.spell.caster,
                self.spell,
                duration,
                damage,
                level.tiles[point.x][point.y].is_chasm,
            )
            level.add_obj(hazard, point.x, point.y)


class PureEtherSphere(Spell):
    def on_init(self):
        self.name = "Pure Ether Sphere"
        self.asset = ["EtherealPack", "pure_ether_sphere_spell"]
        self.minion_damage = 5
        self.range = 9
        self.radius = 1
        self.max_charges = 7
        self.pure_discharge = 0
        self.duration = 7
        self.requires_los = False
        self.melt_walls = True
        self.minion_health = 15
        self.element = Ethereal
        self.damage_type = [Ethereal]
        self.tags = [Ethereal, Tags.Orb, Tags.Conjuration]
        self.level = 4

        self.upgrades["range"] = (5, 2)
        self.upgrades["radius"] = (1.5, 2)
        self.upgrades["minion_damage"] = (9, 3)
        self.upgrades["pure_discharge"] = (
            1,
            4,
            "Pure Discharge",
            "Every 3 turns, the sphere [stuns:physical] up to 3 enemies in line of sight for 2 turns and spreads Pure Ether around them.",
        )

    def make_orb(self, destination=None):
        orb = Orb()
        orb.name = "Pure Ether Sphere"
        orb.asset = ["EtherealPack", "pure_ether_sphere"]
        for res in orb.resists:
            orb.resists[res] = 100
        orb.resists[Ethereal] = 0
        orb.shields = 3
        orb.buffs.append(PureEtherSphereBuff(self, destination))
        apply_minion_bonuses(self, orb)
        return orb

    def can_cast(self, x, y):
        level = self.caster.level
        path = level.get_points_in_line(
            Point(self.caster.x, self.caster.y), Point(x, y)
        )
        if len(path) < 2:
            return False

        start_point = path[1]
        if level.get_unit_at(start_point.x, start_point.y):
            return False

        if not self.get_stat("melt_walls"):
            for point in path:
                if level.tiles[point.x][point.y].is_wall():
                    return False

        return Spell.can_cast(self, x, y)

    def cast(self, x, y):
        level = self.caster.level
        path = level.get_points_in_line(
            Point(self.caster.x, self.caster.y), Point(x, y)
        )
        if len(path) < 2:
            return

        start_point = path[1]
        if level.get_unit_at(start_point.x, start_point.y):
            return

        if self.get_stat("melt_walls") and level.tiles[
            start_point.x
        ][start_point.y].is_wall():
            level.make_floor(start_point.x, start_point.y)

        orb = self.make_orb(Point(x, y))
        orb.turns_to_death = len(path) + 1
        self.summon(orb, target=start_point, radius=0)
        yield

    def get_impacted_tiles(self, x, y):
        return self.caster.level.get_points_in_line(
            Point(self.caster.x, self.caster.y), Point(x, y)
        )[1:]

    def get_extra_examine_tooltips(self):
        return [self.make_orb()] + self.get_upgrade_tooltips()

    def get_description(self):
        return (
            "Summon a Pure Ether Sphere next to you. Each turn, it moves one tile toward the target, melting walls in its path and spreading Pure Ether across a [{radius}:radius] radius.\n"
            "Pure Ether deals [{minion_damage}_Äthereal:äthereal] damage and applies [Ätherealness:äthereal] for [{duration}:duration] turns. The sphere disappears after reaching its destination."
        ).format(**self.fmt_dict())
