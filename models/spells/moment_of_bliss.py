from Level import *
from mods.EtherealPack.models.hazards.bliss_stasis import BlissStasis
from mods.EtherealPack.models.hazards.util import (
    get_hazard_point,
    prepare_stasis_unit,
)
from mods.EtherealPack.tags.Ethereal import Ethereal


class MomentOfBliss(Spell):
    def on_init(self):
        self.name = "A Moment in Heaven"
        self.range = 7
        self.tags = [Ethereal, Tags.Holy, Tags.Enchantment, Tags.Translocation]
        self.level = 2

        self.duration = 7
        self.damage = 3
        self.radius = 7

        self.max_charges = 21
        self.can_target_empty = False
        self.requires_los = False

        # TODO make this only affect the time spent inside not the bonuses of the hazard / aura
        self.upgrades["duration"] = (-4, 1)
        self.upgrades["blind"] = (
            1,
            3,
            "Blinding Grace",
            f"[Blinds:holy] enemies in [{self.radius}_radius:radius] for 3 turns every turn",
        )
        self.upgrades["bless"] = (
            1,
            5,
            "Blessing",
            "Your ally gains [100% Holy:holy] resistance, a ranged attack that deals [7_holy:holy] damage with [7_range:range] range, and [3 HP:heal] regeneration",
            [Tags.Holy],
        )

    def can_cast(self, x, y):
        unit = self.caster.level.get_unit_at(x, y)
        if unit and (
            are_hostile(unit, self.caster)
            or get_hazard_point(self.caster.level, x, y, flying=unit.flying) is None
        ):
            return False
        return super().can_cast(x, y)

    def cast(self, x, y):
        unit = self.caster.level.get_unit_at(x, y)
        hazard_point = get_hazard_point(self.caster.level, x, y, flying=unit.flying)

        unit_in_stasis = prepare_stasis_unit(unit, self.get_stat("duration"))
        stasis = BlissStasis(
            self.caster,
            self,
            self.get_stat("duration"),
            self.get_stat("radius"),
            self.get_stat("damage"),
            unit_in_stasis,
            self.get_stat("blind"),
            self.get_stat("bless"),
        )
        self.caster.level.add_hazard(stasis, hazard_point.x, hazard_point.y)

        yield

    def get_description(self):
        return "Transport an ally into the Plane of Bliss for [{duration}_turns:duration]. The ally restores [{damage}_hp:heal] HP each turn until it reappears.\nLeaves behind a Bliss Rift that heals allies for [{damage}_hp:heal] HP each turn within [{radius}_tile:range] and applies [Ätherealness:äthereal] to units on it for 2 turns.".format(
            **self.fmt_dict()
        )
