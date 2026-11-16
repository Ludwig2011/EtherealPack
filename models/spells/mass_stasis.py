import random

from CommonContent import BleedBuff, FrozenBuff, PetrifyBuff, Poison
from Level import *
from Monsters import HemorrhageBuff
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.stasis import Stasis
from mods.EtherealPack.models.hazards.util import (
    get_hazard_point,
    prepare_stasis_unit,
)
from mods.EtherealPack.tags.Ethereal import Ethereal


class MassStasis(Spell):
    def on_init(self):
        self.name = "Mass Stasis"
        self.range = 10
        self.tags = [Ethereal, Tags.Enchantment, Tags.Translocation]
        self.level = 3

        self.duration = 7
        self.radius = 4
        self.damage_type = [Ethereal]

        self.max_charges = 7

        self.upgrades["radius"] = (2, 2)
        self.upgrades["linger"] = (
            1,
            2,
            "Äther Lag",
            "Targets are also affected by [Ätherealness:äthereal] for the same duration after they return",
        )
        self.upgrades["chaotic_return"] = (
            1,
            3,
            "Äther Scramble",
            "Returning enemies receive a random debuff for the duration of Mass Stasis",
            [Tags.Chaos],
        )
        self.upgrades["entanglement"] = (
            1,
            4,
            "Entanglement",
            "Returning enemies receive [Shared Pain] for the duration of Mass Stasis",
        )

        self.return_debuffs = [
            Poison,
            BleedBuff,
            NecrosisBuff,
            BerserkBuff,
            HemorrhageBuff,
            Silence,
            Stun,
            FrozenBuff,
            PetrifyBuff,
        ]

    def can_cast(self, x, y):
        unit = self.caster.level.get_unit_at(x, y)
        if unit and unit.has_buff(StunImmune):
            return False
        return super().can_cast(x, y)

    def cast(self, x, y):
        for tile in self.caster.level.get_points_in_ball(x, y, self.get_stat("radius")):
            unit = self.caster.level.get_unit_at(tile.x, tile.y)
            if not unit or unit == self.caster:
                continue
            hazard_point = get_hazard_point(
                self.caster.level, unit.x, unit.y, flying=unit.flying
            )
            if not hazard_point:
                continue
            if self.get_stat("linger"):
                unit.apply_buff(EtherealnessBuff(), self.get_stat("duration") * 2)
            unit_in_stasis = prepare_stasis_unit(unit, self.get_stat("duration"))
            stasis = Stasis(
                self.caster,
                self,
                self.get_stat("duration"),
                unit_in_stasis,
                return_debuff=(
                    random.choice(self.return_debuffs)
                    if self.get_stat("chaotic_return") and are_hostile(self.caster, unit)
                    else None
                ),
                shared_pain=self.get_stat("entanglement"),
                return_duration=self.get_stat("duration"),
            )
            self.caster.level.add_hazard(stasis, hazard_point.x, hazard_point.y)

        yield

    def get_description(self):
        return "Transport all targets in a [{radius}_tile:radius] radius into the Ether Plane for [{duration}_turns:duration].\nLeaves behind a Rift that applies [Ätherealness:äthereal] to units for 2 turns.".format(
            **self.fmt_dict()
        )
