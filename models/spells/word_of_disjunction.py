from CommonContent import SimpleRangedAttack, TeleportyBuff
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

class WordOfDisjunction(Spell):

    def on_init(self):
        self.name = "Word of Disjunction"
        self.tags = [Ethereal, Tags.Word]
        self.asset = ['EtherealPack', 'word_of_disjunction']
        self.level = 7

        self.duration = 7
        self.max_charges = 2
        self.range = 0

        self.upgrades['shield_strip'] = (1, 7, "Recombobulate", "Steal 7 shields of all units", None, [])
        self.upgrades['summon_ghosts'] = (1, 7, "Manifest", "Summon an Äther Ghost next to every unit", None, [Tags.Conjuration])



    def cast(self, x, y):
        for unit in self.caster.level.units:
            if not unit == self.caster:
                if are_hostile(self.caster, unit) and Tags.Arcane in unit.tags:
                    continue
                unit.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
                unit.resists[Tags.Physical] = 0
            if self.get_stat('shield_strip'):
                add_shields = min(7, unit.shields)
                self.caster.shields = min(20, self.caster.shields + add_shields)
                unit.shields = max(0, unit.shields - 7)
            if self.get_stat('summon_ghosts'):
                spirit = Unit()
                spirit.name = "Äther Ghost"
                spirit.max_hp = 7 + self.get_stat('minion_health')
                spirit.spells.append(SimpleRangedAttack(damage=7 + self.get_stat('minion_damage'), damage_type=Tags.Ethereal, range=7 + self.get_stat('minion_range')))
                spirit.tags = [Tags.Ethereal, Tags.Undead]
                spirit.buffs.append(TeleportyBuff())
                spirit.resists[Tags.Holy] = 100
                spirit.resists[Tags.Dark] = 100
                spirit.resists[Tags.Ethereal] = 50
                spirit.resists[Tags.Physical] = 50
                spirit.resists[Tags.Arcane] = -100
                spirit.flying = True
                self.summon(spirit, Point(x, y))
        yield

    def get_description(self):
        return "All units except the caster lose their [physical:physical] resistance and recieve Ätherealness for [{duration}_turns:duration].".format(**self.fmt_dict())