#gain back charges of spells when ätherealised enemies die
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class CollectDispersion(Equipment):

    def on_init(self):
        self.name = "Collect Dispersion"
        self.tags = [Ethereal]
        self.asset = ['EtherealPack', 'collect_dispersion']
        self.recipe = [(Ethereal, 3), (Tags.Any, 4)]
        self.global_triggers[EventOnDamaged] = self.on_damaged

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
        return "When an enemy affected by Etherealness dies, each of your Ethereal spells has a chance equal to the remaining Etherealness duration to regain a charge. The chance is tripled if Ethereal damage dealt the killing blow."
