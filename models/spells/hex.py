from Level import *
from mods.EtherealPack.models.buffs.hex_buffs import HexBuff, HexDebuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class Hex(Spell):
    def on_init(self):
        self.name = "Hex"
        self.range = 10
        self.tags = [Ethereal, Tags.Dark, Tags.Enchantment]
        self.asset = ["EtherealPack", "hex"]
        self.level = 2

        self.duration = 7
        self.damage = 7
        self.damage_type = [Ethereal, Tags.Dark]
        self.resist_loss = 25

        self.max_charges = 14

        self.upgrades["resist_loss"] = (25, 2)
        self.upgrades["deterioration"] = (
            1,
            2,
            "Deterioration",
            "Targets affected by Hex also lose [Physical:physical], [Poison:poison], and [Ice:ice] resistance".format(
                **self.fmt_dict()
            ),
        )
        self.upgrades["perpetual_curse"] = (
            1,
            3,
            "Perpetual Curse",
            "When a target affected by both Hex and [Ätherealness:äthereal] dies, reapply Hex to the closest enemy in line of sight.",
        )
        self.upgrades["volatile_death"] = (
            1,
            4,
            "Volatile Death",
            "When a target affected by Hex dies, cause an explosion in a [5_tile:radius] radius that deals [7_dark:dark] and [7_äthereal:äthereal] damage and applies [Ätherealness:äthereal] for [{duration}_turns:duration]".format(
                **self.fmt_dict()
            ),
        )

    def cast(self, x, y):
        unit = self.caster.level.get_unit_at(x, y)
        unit.apply_buff(
            HexDebuff(self.get_stat("resist_loss"), self.get_stat("deterioration")),
            self.get_stat("duration"),
        )
        self.caster.apply_buff(
            HexBuff(
                self.get_stat("damage"),
                self.get_stat("volatile_death"),
                self.get_stat("perpetual_curse"),
                self.get_stat("resist_loss"),
                self.get_stat("deterioration"),
                self.get_stat("duration"),
            ),
            self.get_stat("duration"),
        )
        yield

    def can_cast(self, x, y):
        return self.caster.level.get_unit_at(x, y) and Spell.can_cast(self, x, y)

    def get_description(self):
        description = (
            "Curse an enemy to take [{damage}_äthereal:äthereal] and [{damage}_dark:dark] damage whenever it takes damage for [{duration}_turns:duration]. It also loses {} [Dark:dark] and [Äthereal:äthereal] resistance.".format(
                self.resist_loss, **self.fmt_dict()
            )
        )
        return description
