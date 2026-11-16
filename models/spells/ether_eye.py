from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.spells.hex import Hex
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherEyeBuff(Buff):
    def __init__(self, spell):
        Buff.__init__(self)
        self.name = "Elemental Eye"
        self.color = Ethereal.color
        self.requires_los = spell.get_stat("requires_los")
        self.asset = ["EtherealPack", "ether_eye_buff"]
        self.damage_type = Ethereal
        self.damage = spell.get_stat("damage")
        self.freq = spell.get_stat("shot_cooldown")
        self.cooldown = self.freq
        self.shield_burn = spell.get_stat("shield_burn")
        self.focus_weak = spell.get_stat("focus_weak")
        self.ally_bolts = spell.get_stat("ally_bolts")
        self.cast_hex = spell.get_stat("cast_hex")

    def on_advance(self):
        self.cooldown -= 1
        if self.cooldown == 0:
            self.cooldown = self.freq

            if self.get_targets(self.owner) or any(
                self.get_targets(ally) for ally in self.get_allies()
            ):
                self.owner.level.queue_spell(self.shoot())
            else:
                self.cooldown = 1

    def get_targets(self, source):
        level = self.owner.level
        if self.requires_los:
            targets = level.get_units_in_los(source)
        else:
            targets = level.units
        targets = [
            unit
            for unit in targets
            if unit.is_alive() and are_hostile(unit, source)
        ]
        if self.focus_weak and targets:
            lowest_resist = min(unit.resists[self.damage_type] for unit in targets)
            targets = [
                unit
                for unit in targets
                if unit.resists[self.damage_type] == lowest_resist
            ]
        return targets

    def get_allies(self):
        return [
            unit
            for unit in list(self.owner.level.units)
            if unit is not self.owner
            and unit.is_alive()
            and not are_hostile(unit, self.owner)
            and (Ethereal in unit.tags or unit.has_buff(EtherealnessBuff))
        ]

    def shoot(self):
        possible_targets = self.get_targets(self.owner)
        if possible_targets:
            target = random.choice(possible_targets)
            yield from self.shoot_from(self.owner, Point(target.x, target.y))

        if not self.ally_bolts:
            return

        for ally in self.get_allies():
            if not ally.is_alive():
                continue
            possible_targets = self.get_targets(ally)
            if possible_targets:
                target_unit = random.choice(possible_targets)
                yield from self.shoot_from(
                    ally, Point(target_unit.x, target_unit.y)
                )

    def shoot_from(self, source, target):
        level = self.owner.level
        path = self.owner.level.get_points_in_line(
            Point(source.x, source.y), target, find_clear=self.requires_los
        )

        for point in path:
            level.deal_damage(point.x, point.y, 0, self.damage_type, self)
            yield

        unit = level.get_unit_at(target.x, target.y)
        if unit and self.shield_burn:
            unit.shields = max(0, unit.shields - self.shield_burn)
        level.deal_damage(target.x, target.y, self.damage, self.damage_type, self)

        if self.cast_hex and unit and unit.is_alive():
            hex_spell = self.owner.get_or_make_spell(Hex)
            yield from level.act_cast(
                self.owner, hex_spell, unit.x, unit.y, pay_costs=False, queue=False
            )


class EyeOfEtherSpell(Spell):
    def on_init(self):
        self.range = 0
        self.max_charges = 4
        self.name = "Eye of Äther"
        self.asset = ["EtherealPack", "ether_eye"]
        self.requires_los = True
        self.damage = 15
        self.damage_type = [Ethereal]
        self.element = Ethereal
        self.duration = 30
        self.shot_cooldown = 3
        self.shield_burn = 0
        self.focus_weak = 0
        self.ally_bolts = 0
        self.cast_hex = 0
        
        self.stats.append('shot_cooldown')

        self.upgrades["shield_burn"] = (
            3,
            2,
            "Shield Burn",
            "The Eye removes 3 [SH:shields] from each target before dealing damage",
        )
        self.upgrades["focus_weak"] = (
            1,
            2,
            "Ether Focus",
            "The Eye prioritizes enemies with the lowest [äthereal:äthereal] resistance",
        )
        self.upgrades["ally_bolts"] = (
            1,
            5,
            "Ether Refraction",
            "Each allied [Äthereal] or [Ätherealiesed:äthereal] unit also fires a bolt at a random hostile enemy",
        )
        self.upgrades["cast_hex"] = (
            1,
            4,
            "Cursed Gaze",
            "The Eye also casts your Hex on each target without spending a charge",
            [Tags.Dark],
        )

        self.tags = [Ethereal, Tags.Enchantment, Tags.Eye]
        self.level = 2

    def cast_instant(self, x, y):
        buff = EtherEyeBuff(self)
        buff.element = self.element
        self.caster.apply_buff(buff, self.get_stat("duration"))

    def get_description(self):
        return (
            "Every [{shot_cooldown}_turns:shot_cooldown], deals [{damage}_äthereal:äthereal] damage to a random enemy unit in line of sight.\n"
            "Lasts [{duration}_turns:duration]."
        ).format(**self.fmt_dict())
