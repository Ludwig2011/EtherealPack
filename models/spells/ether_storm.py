import random

from CommonContent import FrozenBuff
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherStormSpell(Spell):
    def on_init(self):

        self.name = "Äther Storm"
        self.level = 2
        self.asset = ["EtherealPack", "ether_storm"]

        self.num_targets = 7
        self.range = 7
        self.max_charges = 7
        self.damage = 7
        self.radius = 7
        self.duration = 2
        self.requires_los = True
        self.damage_type = [Ethereal, Tags.Lightning]

        self.upgrades["requires_los"] = (
            -1,
            2,
            "Blindcasting",
            "Äther Storm can be cast without line of sight",
        )
        self.upgrades["endothermic_discharge"] = (
            1,
            2,
            "Endothermic Discharge",
            "The bolts freeze enemies for 1 turn",
            [Tags.Ice],
        )
        self.upgrades["lingering_static"] = (
            1,
            2,
            "Lingering Static",
            "The Storms static field applies Ätherealness to all units for [{duration}_turns:duration]",
        )
        self.upgrades["searing_storm"] = (
            1,
            2,
            "Searing Storm",
            "The bolts leave enemies with burns dealing [{damage}_fire:fire] damage for 3 turns",
            [Tags.Fire],
        )

        self.tags = [Tags.Sorcery, Tags.Chaos, Tags.Lightning, Ethereal]

    def get_description(self):
        description = (
            "Open a Rift to the Energy Plane through which {} energy bolts strike random enemies in [{radius}_radius:radius]\n"
            "Each bolt deals [{damage}_äthereal:äthereal] damage and deals lightning damage against [ätherealiesed:äthereal] targets aswell"
        )
        return description.format(self.get_stat("num_targets"), **self.fmt_dict())

    def cast(self, x, y):
        targets = [
            u
            for u in self.caster.level.get_units_in_ball(
                Point(x, y), self.get_stat("radius")
            )
            if u != self.caster and are_hostile(self.caster, u)
        ]

        for i in range(self.get_stat("num_targets")):
            if len(targets) < 1:
                continue
            target = random.choice(targets)
            if self.get_stat("endothermic_discharge"):
                target.apply_buff(FrozenBuff(), 1)
            if self.get_stat("searing_storm"):
                target.apply_buff(EtherBuff(self.get_stat("damage")), 3)
            if target.has_buff(EtherealnessBuff()):
                self.caster.level.deal_damage(
                    target.x, target.y, self.damage, Tags.Lightning, self
                )
            self.caster.level.deal_damage(
                target.x, target.y, self.damage, Ethereal, self
            )
            if target.cur_hp < 1:
                targets.remove(target)

        targets = [
            u
            for u in self.caster.level.get_units_in_ball(
                Point(x, y), self.get_stat("radius")
            )
            if u.cur_hp > 0
        ]
        if self.get_stat("lingering_static"):
            for target in targets:
                target.apply_buff(EtherealnessBuff(), self.get_stat("duration"))
        yield


class EtherBuff(Buff):
    def __init__(self, damage):
        self.damage = damage
        Buff.__init__(self)

    def on_init(self):
        self.name = f"Burning ({self.damage})"
        self.description = (
            f"At end of this units turn, it takes {self.damage} damage."
        )
        self.asset = ["status", "burning"]

    def on_advance(self):
        self.owner.deal_damage(self.damage, Tags.Fire, self)
