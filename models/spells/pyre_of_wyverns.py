from CommonContent import SimpleMeleeAttack
from Level import *
from mods.EtherealPack.models.minions.ether_wave import EtherWave
from mods.EtherealPack.models.minions.ether_wyvern import EtherWyvern
from mods.EtherealPack.tags.Ethereal import Ethereal


class PyreOfWyvernsSpell(Spell):
    def on_init(self):

        self.name = "Pyre of Wyverns"
        self.level = 5

        self.minion_health = 10
        self.minion_damage = 3
        self.breath_damage = 0
        self.minion_range = 4
        self.num_summons = 4
        self.shields = 2
        self.max_charges = 2

        self.upgrades["shields"] = (5, 2)
        self.upgrades["num_summons"] = (3, 4)
        self.upgrades["shielding_waves"] = (
            1,
            4,
            "Embracing Waves",
            "The Wyverns' Äther Waves grant allies up to [2 SH:shields].",
        )
        self.upgrades["ether_link"] = (
            1,
            5,
            "Link",
            "Wyverns link to each other when nearby, increasing their radius by [3:radius] and reducing their wave cooldown to [2_turns:duration].",
        )

        self.range = 0
        self.tags = [Tags.Dragon, Tags.Conjuration, Ethereal]

    def get_description(self):
        return (
            "Summons [{num_summons}_wyverns:num_summons] near the caster.\n"
            "Wyverns have [{minion_health}_HP:minion_health], [{shields}_SH:shields], and [50% Äthereal:äthereal], [25% Physical:physical], and [-25% Arcane:arcane] resistance.\n"
            "Wyverns have an Äther Wave attack that deals [{minion_damage}_äthereal:äthereal] damage in a [4_tile:radius] radius and applies [Ätherealness:äthereal] for 3 turns.\n"
            "Wyverns have a melee attack which deals [{minion_damage}_physical:physical] damage."
        ).format(**self.fmt_dict())

    def make_wyvern(self):
        wyvern = EtherWyvern(shields=self.get_stat("shields"))
        wyvern.max_hp = self.get_stat("minion_health")
        wyvern.spells.clear()
        wyvern.spells.append(
            EtherWave(
                self.get_stat("minion_damage") + self.get_stat("breath_damage"),
                self.get_stat("minion_range"),
                self.get_stat("shielding_waves"),
                self.get_stat("ether_link"),
            )
        )
        wyvern.spells.append(SimpleMeleeAttack(self.get_stat("minion_damage")))
        return wyvern

    def get_extra_examine_tooltips(self):
        return [self.make_wyvern()] + self.get_upgrade_tooltips()

    def cast_instant(self, x, y):
        for i in range(self.get_stat("num_summons")):
            wyvern = self.make_wyvern()
            wyvern.team = self.caster.team
            self.summon(wyvern, Point(x, y))
