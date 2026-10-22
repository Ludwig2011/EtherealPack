from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class EtherBolt(Spell):  # energy_disruption when self is Ätherealiesed aswell/instead?
    def on_init(self):
        self.name = "Äther Bolt"
        self.range = 8
        self.tags = [Ethereal, Tags.Sorcery]
        self.asset = ["EtherealPack", "ether_bolt"]
        self.level = 1

        self.damage = 11
        self.duration = 3
        self.damage_type = [Ethereal]
        self.can_target_empty = False

        self.max_charges = 21
        self.has_hit = []

        self.upgrades[("damage", "range", "hp_cost")] = (
            [11, 5, 1],
            2,
            "Energy Expense",
            None,
            [Tags.Blood],
            None,
        )
        self.upgrades["energy_drain"] = (
            5,
            2,
            "Energy Drain",
            "If Äther Bolt targets a unit affected by Ätherealness, it grants you a shield up to maximum of 5",
        )
        self.upgrades["energy_disruption"] = (
            1,
            4,
            "Energy Disruption",
            f"If Äther Bolt targets a unit affected by Ätherealness, it deals {int(self.damage / 2)} [fire], [lightning], and [ice] aswell",
            [Tags.Chaos],
            [Tags.Fire, Tags.Lightning, Tags.Ice],
        )
        self.upgrades["energy_connection"] = (
            1,
            6,
            "Energy Connection",
            "If Äther Bolt targets a unit affected by Ätherealness, Äther Bolt is cast again at units affected by Ätherealness in line of sight.",
        )

    def cast(self, x, y):
        dtypes = []
        to_hit_list = []
        unit = self.caster.level.get_unit_at(x, y)
        original = not self.has_hit
        self.has_hit.append(unit)

        for p in self.caster.level.get_points_in_line(
            self.caster, Point(x, y), find_clear=True
        )[1:-1]:
            self.caster.level.show_effect(p.x, p.y, Ethereal, minor=True)

        if unit and unit.has_buff(EtherealnessBuff):
            if (
                self.get_stat("energy_drain")
                and self.caster.shields < self.get_stat("energy_drain")
            ):
                self.caster.shields += 1
            if self.get_stat("energy_disruption"):
                dtypes = [Tags.Fire, Tags.Lightning, Tags.Ice]
            if self.get_stat("energy_connection"):
                for u in self.caster.level.get_units_in_los(unit):
                    if (
                        u not in self.has_hit
                        and u.is_alive()
                        and u.has_buff(EtherealnessBuff)
                        and are_hostile(self.caster, u)
                    ):
                        to_hit_list.append(u)
        self.caster.level.deal_damage(x, y, self.get_stat("damage"), Ethereal, self)
        for dtype in dtypes:
            self.caster.level.deal_damage(
                x, y, self.get_stat("damage") / 2, dtype, self
            )
        if unit and unit.resists[Ethereal] < 100:
            unit.apply_buff(EtherealnessBuff(), self.get_stat("duration"))
        for u in to_hit_list:
            self.caster.level.act_cast(
                self.caster,
                self.caster.get_or_make_spell(EtherBolt),
                u.x,
                u.y,
                pay_costs=False,
            )

        if original:
            self.has_hit.clear()
        yield

    def get_description(self):
        return "Deal [{damage}_äthereal:äthereal] damage to the target and apply Ätherealness for [{duration}_turns:duration].".format(
            **self.fmt_dict()
        )
