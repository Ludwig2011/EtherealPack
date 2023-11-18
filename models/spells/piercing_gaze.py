from CommonContent import PetrifyBuff, Poison
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class PiercingGaze(Spell):

    def on_init(self):
        self.name = "Piercing Gaze"

        self.range = 0
        self.max_charges = 4
        self.duration = 10
        self.damage = 1

        self.tags = [Ethereal, Tags.Nature, Tags.Sorcery]
        self.level = 3
        self.upgrades['damage'] = (6, 4)
        self.upgrades['duration'] = (10, 2)
        self.upgrades['max_charges'] = (3, 1)
        self.upgrades['unnerving_gaze'] = (1, 3, "Unnerving Gaze", "Ätherealies enemies aswell")
        self.upgrades['shocking_gaze'] = (1, 3, "Shocking Gaze", "Petrify affected enemies for 1 turn")



    def get_description(self):
        return ("[Poison:poison] all enemies in line of sight of the caster for [{duration}_turns:duration].\n"
                "Deals [{damage}_äthereal:äthereal] and [{damage}_physical:physical] damage to affected enemies.").format(**self.fmt_dict())

    def cast(self, x, y):
        targets = [u for u in self.caster.level.get_units_in_los(self.caster) if u != self.caster and are_hostile(u, self.caster)]
        #targets = sorted(targets, key=lambda u: distance(u, self.caster))

        for target in targets:
            target.apply_buff(Poison(), self.get_stat('duration'))
            target.deal_damage(self.get_stat('damage'), Tags.Physical, self)
            target.deal_damage(self.get_stat('damage'), Ethereal, self)
            if target.cur_hp > 0: 
                if self.get_stat('unnerving_gaze'):
                    target.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
                if self.get_stat('shocking_gaze'):
                    target.apply_buff(PetrifyBuff(), 1)
            yield