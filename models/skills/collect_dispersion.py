#gain back charges of spells when ätherealised enemies die
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class CollectDispersion(Upgrade):

    def on_init(self):
        self.global_triggers[EventOnDamaged] = self.on_damaged
        self.name = "Collect Dispersion"
        self.tags = [Ethereal]
        self.asset = ['EtherealPack', 'collect_dispersion']
        self.level = 6

    def on_damaged(self, damage_event):

        # No harvesting your summons
        if not self.owner.level.are_hostile(self.owner, damage_event.unit):
            return

        if damage_event.unit.cur_hp <= 0 and damage_event.unit.has_buff(EtherealnessBuff):
            chance = 0
            for buff in damage_event.unit.buffs:
                if isinstance(buff, EtherealnessBuff):
                    chance = buff.turns_left
            if damage_event.damage_type == Ethereal:
                chance *= 3
            for spell in self.owner.spells:
                if random.random()*100 < chance:
                    if Ethereal in spell.tags and spell.cur_charges < spell.get_stat('max_charges'):
                        spell.cur_charges += 1
                        self.owner.level.show_effect(self.owner.x, self.owner.y, Ethereal)

    def get_description(self):
        return ("Whenever an enemy unit dies, each of your [äthereal] spells has a chance euqal to 1/100 of the Ätherealness applied to the unit to gain a charge.\n"
                "This chance is tripled if the unit died to [äthereal] damage.")
