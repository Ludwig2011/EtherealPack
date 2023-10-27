from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class WordOfDisjunction(Spell):

    def on_init(self):
        self.name = "Word of Disjunction"
        self.tags = [Ethereal, Tags.Word]
        self.level = 1

        self.duration = 7
        self.max_charges = 2
        self.range = 0

        self.upgrades['max_charges'] = (5, 3)
        self.upgrades['duration'] = (7, 2)


    def cast(self, x, y):
        for unit in self.caster.level.units:
            if not unit == self.caster:
                unit.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
                unit.resists[Tags.Physical] = 0
        yield

    def get_description(self):
        return "All units except the caster lose their [physical:physical] resistance and recieve Ätherealness for [{duration}_turns:duration].".format(**self.fmt_dict())