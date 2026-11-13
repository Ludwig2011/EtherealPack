from CommonContent import SimpleRangedAttack
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.tags.Ethereal import Ethereal


def ÄtherImp():
    unit = Unit()
    unit.asset = ["EtherealPack", "ether_imp"]
    unit.name = "Äther Imp"
    unit.tags = [Tags.Demon, Ethereal]
    unit.resists[Ethereal] = 100
    unit.resists[Tags.Physical] = 75
    unit.resists[Tags.Dark] = 50
    unit.resists[Tags.Holy] = 50
    unit.resists[Tags.Arcane] = -100
    unit.flying = True
    unit.shields = 1
    unit.max_hp = 7
    unit.spells.append(
        SimpleRangedAttack(
            "Äther Bolt", 7, Ethereal, 5, buff=EtherealnessBuff, buff_duration=3
        )
    )
    return unit


class EtherStream(Spell):
    def on_init(self):
        self.requires_los = False
        self.range = 99
        self.name = "Äther Stream"
        self.max_charges = 12
        self.asset = ["EtherealPack", "ether_stream"]
        self.tags = [Ethereal, Tags.Sorcery, Tags.Translocation]
        self.level = 3

        self.upgrades[('imp', 'num_summons', 'minion_health', 'minion_damage', 'minion_range')] = (
            [1, 3, 7, 3, 4],
            3,
            "Imp Friends",
            "Summon [{num_summons}:num_summons] Äther Imps at the beginning and end of the stream. They gain [{minion_health}:minion_health] bonus HP and [{minion_damage}:minion_damage] damage",
            [Tags.Conjuration]
        )
        self.add_upgrade(NetherAlone())
        self.upgrades[('make_home', 'radius')] = ([1, 5], 2, "Make Home", "Create hazards that [ätherealies:äthereal] units in a [{radius}_tile:radius] radius at the destination")

    def get_description(self):
        return (
            "Jump out of the Äther Stream found next to an [Äther:äthereal] or [ätherealiesed:äthereal] unit"
            "Teleport to any tile adjacent to an [Äther:äthereal] or [ätherealiesed:äthereal] unit.\n"
            "Can only be cast while adjacent to an [Äther:äthereal] or [ätherealiesed:äthereal] unit."
        ).format(**self.fmt_dict())

    def can_cast(self, x, y):

        if not self.caster.level.can_stand(x, y, self.caster):
            return False

        next_to_äther = False
        for p in self.caster.level.get_points_in_ball(
            x, y, 1.5, diag=True
        ):
            unit = self.caster.level.tiles[p.x][p.y].unit
            if unit and (unit.has_buff(EtherealnessBuff) or Ethereal in unit.tags):
                next_to_äther = True
                break
        if not next_to_äther:
            return False
        return Spell.can_cast(self, x, y)

    def cast_instant(self, x, y):

        old_loc = Point(self.caster.x, self.caster.y)
        self.caster.level.act_move(self.caster, x, y, teleport=True)

        radius = self.get_stat("radius")
        if radius:
            for point in self.caster.level.get_points_in_ball(
                x, y, radius
            ):
                tile = self.caster.level.tiles[point.x][point.y]

                if not tile.is_wall() and tile.prop is None:
                    pure_ether = PureEther(
                        self.caster,
                        self,
                        7,
                        0,
                        tile.is_chasm
                    )
                    self.caster.level.add_obj(
                        pure_ether, point.x, point.y
                    )

        for point in [old_loc, self.caster]:
            for i in range(self.get_stat("num_summons")):
                p = self.caster.level.get_summon_point(
                    point.x, point.y, sort_dist=True
                )
                if p:
                    imp = ÄtherImp()
                    imp.max_hp = self.get_stat("minion_health")
                    imp.spells[0].damage = self.get_stat("minion_damage")
                    imp.spells[0].range = self.get_stat("minion_range")
                    imp.team = self.caster.team
                    self.summon(imp, p)

class NetherAlone(Upgrade):

    def on_init(self):
        self.level = 6
        self.name = "Nether Alone"
        self.description = "When an [ätherealiesed:äthereal] enemy dies, summon an Äther Imp with remaining turns equal to the debuff.\nAlways Active"
        self.tags = [Tags.Conjuration]
        self.global_triggers[EventOnDeath] = self.on_death

    def on_death(self, evt):
        unit = evt.unit
        if not unit or unit.team == self.owner.team:
            return

        buff = unit.get_buff(EtherealnessBuff)
        if not buff:
            return

        p = self.owner.level.get_summon_point(
            unit.x, unit.y, sort_dist=True
        )

        if not p:
            return

        imp = ÄtherImp()
        imp.max_hp = self.prereq.get_stat("minion_health")
        imp.spells[0].damage = self.prereq.get_stat("minion_damage")
        imp.spells[0].range = self.prereq.get_stat("minion_range")
        imp.team = self.owner.team
        imp.turns_to_death = buff.turns_left + 1

        self.summon(imp, p)
                    