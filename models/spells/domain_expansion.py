from Level import *
from mods.EtherealPack.models.hazards.pure_ether import PureEther
from mods.EtherealPack.tags.Ethereal import Ethereal


class DomainExpansion(Spell):

    def on_init(self):

        self.name = "Domain Expansion"
        
        self.level = 6
        self.max_charges = 0
        self.duration = 7
        self.cool_down = 21

        self.radius = 4

        self.shielding = 0 #might have base functionality?

        self.stun = 1


        self.upgrades['duration'] = (7, 1)
        self.upgrades['radius'] = (3, 2)
        self.upgrades['stun'] = (2, 3)
        self.upgrades['shielding'] = (1, 1)

        self.tags = [Tags.Sorcery, Ethereal]


    def get_description(self):
        return ("Expand your domain in a [{radius}_tile:radius] radius stunning all enemies present for [{stun}_turns:stun]\n"
                "Leave behind hazards in the same radius for [{duration}_turns:duration] that apply [Ätherealness:äthereal] for [2_turns:duration]\n"
                "This spell has a 21 turn cooldown instead of charges").format(**self.fmt_dict())

    def cast_instant(self, x, y):
        hostile_targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u != self.caster and are_hostile(self.caster, u)]
        friendly_targets = [u for u in self.caster.level.get_units_in_ball(Point(x, y), self.radius) if u != self.caster and not are_hostile(self.caster, u)]
        for target in hostile_targets:
            target.apply_buff(Stun(), self.get_stat("stun"))
        
        if self.get_stat("shielding"):
            for target in friendly_targets:
                if target.shields < 2:
                    target.shields += 1

        for point in self.caster.level.get_points_in_ball(x, y, self.radius):
            if self.caster.level.tiles[point.x][point.y].prop == None:
                pure_ether = PureEther(self.caster,self,self.get_stat('duration'),0,self.caster.level.tiles[point.x][point.y].is_chasm)
                self.caster.level.add_obj(pure_ether, point.x, point.y)
