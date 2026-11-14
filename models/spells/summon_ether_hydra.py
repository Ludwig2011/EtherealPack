# Consitent naming scheme required
from CommonContent import RegenBuff
from Level import *
from mods.EtherealPack.models.buffs.lost_heads_buff import (
    LostHeadsBuff,
    make_lost_head as make_lost_head_unit,
)
from mods.EtherealPack.models.minions.ether_hydra import EtherHydra
from mods.EtherealPack.models.spells.ether_bolt import EtherBolt
from mods.EtherealPack.tags.Ethereal import Ethereal


class SummonEtherHydraSpell(Spell):
    def on_init(self):
        self.name = "Äther Hydra"
        self.range = 4
        self.max_charges = 3
        self.asset = ["EtherealPack", "ether_hydra_spell"]
        self.tags = [Ethereal, Tags.Conjuration, Tags.Dragon]
        self.level = 4

        self.minion_health = 45
        self.minion_damage = 9
        self.minion_range = 7
        self.minion_regen = 3
        self.upgrades["minion_regen"] = (4, 1)
        self.upgrades["element_mother"] = (
            1,
            3,
            "Element Mother",
            "Each of the Äther Hydra's Äther Beams also deals [Fire:fire], [Lightning:lightning], or [Ice:ice] damage.\nThe Hydra gains [50% Fire:fire], [50% Lightning:lightning], and [50% Ice:ice] resistance.",
            [Tags.Chaos],
        )
        self.upgrades["lost_heads"] = (
            1,
            3,
            "Lost Heads",
            "Whenever the Hydra loses [15 HP:damage], it spawns a stationary minion with an Äther Beam attack nearby",
        )
        self.add_upgrade_tooltip("Lost Heads", self.make_lost_head)
        self.upgrades["dragon_mage"] = (
            1,
            6,
            "Dragon Mage",
            "Summoned Äther Hydras can cast Äther Bolt with a 3 turn cooldown.\nThis Äther Bolt gains all of your upgrades and bonuses.",
        )

        self.must_target_empty = True

    def make_hydra(self):
        drake = EtherHydra(self.get_stat("element_mother"))
        drake.max_hp = self.get_stat("minion_health")
        drake.spells[0].damage = self.get_stat("minion_damage")
        drake.spells[0].range = self.get_stat("minion_range")
        drake.spells[1].damage = self.get_stat("minion_damage")

        drake.buffs.append(RegenBuff(self.get_stat("minion_regen")))
        if self.get_stat("lost_heads"):
            drake.buffs.append(
                LostHeadsBuff(
                    self.get_stat("element_mother"), self.get_stat("minion_damage")
                )
            )

        if self.get_stat("dragon_mage"):
            fball = EtherBolt()
            fball.statholder = self.caster
            fball.max_charges = 0
            fball.cur_charges = 0
            fball.cool_down = 3
            drake.spells.insert(0, fball)
        return drake

    def make_lost_head(self):
        return make_lost_head_unit(
            self.get_stat("element_mother"), self.get_stat("minion_damage")
        )

    def get_extra_examine_tooltips(self):
        return [self.make_hydra()] + self.get_upgrade_tooltips()

    def cast_instant(self, x, y):
        drake = self.make_hydra()
        drake.team = self.caster.team
        self.summon(drake, Point(x, y))

    def get_description(self):
        return (
            "Summon an Äther Hydra at target square.\n"
            "Äther Hydras have a breath weapon which deals [{minion_damage}_äthereal:äthereal] damage.\n"
            "Äther Hydras have a melee attack which deals [{minion_damage}_physical:physical] damage.\n"
            "Äther Hydras trample over allies to get where they want"
        ).format(**self.fmt_dict())
