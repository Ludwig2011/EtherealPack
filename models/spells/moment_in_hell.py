from Level import *
from mods.EtherealPack.models.hazards.hell_stasis import HellStasis
from mods.EtherealPack.models.hazards.util import (
    get_hazard_point,
    prepare_stasis_unit,
)
from mods.EtherealPack.tags.Ethereal import Ethereal


class MomentInHell(Spell):  # mordred???????????????????????????????
    def on_init(self):
        self.name = "A Moment in Hell"
        self.range = 7
        self.tags = [Ethereal, Tags.Fire, Tags.Enchantment, Tags.Translocation]
        self.asset = ["EtherealPack", "hell_moment"]
        self.level = 3

        self.duration = 4
        self.damage = 5
        self.damage_type = [Tags.Fire, Ethereal]

        self.max_charges = 11
        self.can_target_empty = False

        self.upgrades["damage"] = (9, 4)
        self.upgrades["duration"] = (3, 1)
        self.upgrades["brimstone"] = (
            1,
            3,
            "Brimstone",
            "Fragments leave behind brimstone hazards for 3 turns that deal [fire:fire] damage",
        )
        self.upgrades["explosive_entry"] = (
            1,
            4,
            "Explosive Entry",
            "When the target reappears or dies in the Fire Plane, deal [Fire:fire] and [Äthereal:äthereal] damage equal to 1/4 of its maximum HP in a radius of round(max HP / 8) if max HP is under 33, or 2 + round(max HP / 16) otherwise. The radius is capped at 10 tiles.",
        )

    def can_cast(self, x, y):
        unit = self.caster.level.get_unit_at(x, y)
        if unit and (
            unit.has_buff(StunImmune)
            or get_hazard_point(self.caster.level, x, y, flying=unit.flying) is None
        ):
            return False
        return super().can_cast(x, y)

    def cast(self, x, y):
        unit = self.caster.level.get_unit_at(x, y)
        hazard_point = get_hazard_point(self.caster.level, x, y, flying=unit.flying)
        unit_in_stasis = prepare_stasis_unit(unit, self.get_stat("duration"))
        stasis = HellStasis(
            self.caster,
            self,
            self.get_stat("duration"),
            self.get_stat("damage"),
            unit_in_stasis,
            self.get_stat("brimstone"),
            self.get_stat("explosive_entry"),
        )
        self.caster.level.add_hazard(stasis, hazard_point.x, hazard_point.y)

        yield

    def get_description(self):
        return "Transport the target into the Plane of Fire for [{duration}_turns:duration]. It takes [{damage}_fire:fire] damage each turn until it reappears.\nLeaves behind a Hell Rift that deals [{damage}_fire:fire] damage to enemies and applies [Ätherealness:äthereal] for 2 turns.\nEach turn, fragments deal [{damage}_fire:fire] and [{damage}_äthereal:äthereal] damage to 3 random enemies in a [5_tile:radius] radius around the rift.".format(
            **self.fmt_dict()
        )
