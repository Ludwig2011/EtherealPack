from Level import *
from mods.EtherealPack.tags.Ethereal import Ethereal


class ExpandingForceBuff(Buff):
    def __init__(self, damage, damage_type, radius, teleport_blocker, collision_damage):
        Buff.__init__(self)
        self.damage = damage
        self.damage_type = damage_type
        self.radius = radius
        self.teleport_blocker = teleport_blocker
        self.collision_damage = collision_damage
        self.source = None
        self.global_triggers[EventOnMoved] = self.on_moved
        self.name = "Expanding Fore Aura"

    def on_advance(self):

        effects_left = 7

        units_to_push = []
        for unit in self.owner.level.get_units_in_ball(
            Point(self.owner.x, self.owner.y), self.radius
        ):
            if unit == self.owner:
                continue

            if not self.owner.level.are_hostile(self.owner, unit):
                continue

            if isinstance(self.damage_type, list):
                damage_type = random.choice(self.damage_type)
            else:
                damage_type = self.damage_type
            unit.deal_damage(self.damage, damage_type, self.source or self)
            # move unit
            units_to_push.append(unit)
            effects_left -= 1
        for unit in units_to_push:
            self.push(unit, self.owner, 1)

        # Show some graphical indication of this aura if it didnt hit much
        points = self.owner.level.get_points_in_ball(
            self.owner.x, self.owner.y, self.radius
        )
        points = [p for p in points if not self.owner.level.get_unit_at(p.x, p.y)]
        random.shuffle(points)
        for i in range(effects_left):
            if not points:
                break
            p = points.pop()
            if isinstance(self.damage_type, list):
                damage_type = random.choice(self.damage_type)
            else:
                damage_type = self.damage_type
            self.owner.level.deal_damage(
                p.x, p.y, 0, damage_type, source=self.source or self
            )

    def on_moved(self, evt):
        if (
            not self.teleport_blocker
            or not evt.teleport
            or not are_hostile(evt.unit, self.owner)
        ):
            return
        units = [
            u
            for u in self.owner.level.get_units_in_ball(
                Point(self.owner.x, self.owner.y), self.radius
            )
        ]
        if evt.unit not in units:
            return
        damage_type = (
            random.choice(self.damage_type)
            if isinstance(self.damage_type, list)
            else self.damage_type
        )
        evt.unit.deal_damage(self.damage, damage_type, self.source or self)
        evt.unit.apply_buff(Stun(), 3)

    def push(self, target, source, squares):
        direction_x = target.x - source.x
        direction_y = target.y - source.y

        new_x = target.x
        new_y = target.y

        if direction_x > 0:
            new_x += squares
        elif direction_x < 0:
            new_x -= squares

        if direction_y > 0:
            new_y += squares
        elif direction_y < 0:
            new_y -= squares

        if target.level.can_move(target, new_x, new_y, teleport=False):
            target.level.act_move(target, new_x, new_y, teleport=False)
            return True
        else:
            if self.collision_damage:
                target.deal_damage(
                    self.collision_damage, Tags.Physical, self.source or self
                )
            return False

    def can_threaten(self, x, y):
        return distance(self.owner, Point(x, y)) <= self.radius

    def get_tooltip(self):
        damage_type_str = (
            " or ".join(t.name for t in self.damage_type)
            if isinstance(self.damage_type, list)
            else self.damage_type.name
        )
        unit_type_str = "enemy units"
        return f"Each turn, deals {self.damage} {damage_type_str} damage to {unit_type_str} in a {self.radius} tile radius and pushes enemies back 1 tile"


class ExpandingForceSpell(Spell):
    def on_init(self):

        self.range = 0
        self.max_charges = 3
        self.name = "Expanding Force"
        self.asset = ["EtherealPack", "expanding_force"]
        self.aura_damage = 2
        self.collision_damage = 0
        self.radius = 5
        self.duration = 7

        self.stats.append("aura_damage")

        self.upgrades["radius"] = (2, 1)
        self.upgrades["collision_damage"] = (
            5,
            2,
            "Collision",
            "When a pushed enemy is blocked by a wall or another unit, it takes [5_physical:physical] damage.",
        )
        self.upgrades["teleport_blocker"] = (
            1,
            3,
            "Teleport Blocker",
            "When an enemy teleports inside this radius, it takes [2_äthereal:äthereal] damage and is [stun]ned for [3_turns:duration].",
        )

        self.tags = [Tags.Enchantment, Ethereal, Tags.Arcane]
        self.level = 4

    def cast_instant(self, x, y):
        buff = ExpandingForceBuff(
            self.get_stat("aura_damage"),
            [Ethereal],
            self.get_stat("radius"),
            self.get_stat("teleport_blocker"),
            self.get_stat("collision_damage"),
        )
        buff.stack_type = STACK_REPLACE
        buff.color = Ethereal.color
        buff.name = "Expanding Force Aura"
        buff.source = self
        self.caster.apply_buff(buff, self.get_stat("duration"))

    def get_description(self):
        return (
            "Each turn, deals [{aura_damage}_äthereal:äthereal] damage to each enemy and push them [1_tile:radius] away from the caster in a [{radius}_tile:radius] radius.\n"
            "This damage is fixed, and cannot be increased using shrines, skills, or buffs.\n"
            "Lasts [{duration}_turns:duration]."
        ).format(**self.fmt_dict())
