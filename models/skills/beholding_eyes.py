from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class BeholdingEyes(Upgrade):#prioritise enemies!
    def __init__(self):
        Upgrade.__init__(self)
        self.name = "Beholding Eyes"
        self.asset = ['EtherealPack', 'beholding_eyes']
        self.tags = [Ethereal, Tags.Eye]
        self.level = 4
        
    def on_advance(self):
        eyes = [u for u in self.owner.level.units if not are_hostile(u, self.owner) and ("Eye" in u.name or Tags.Eye in u.tags or "Lens" in u.name)]

        for eye in eyes:
            enemy_targets = [u for u in self.owner.level.get_units_in_los(eye) if are_hostile(u, self.owner)]
            if len(enemy_targets) > 0:
                target = random.choice(enemy_targets)
            else:
                targets = [u for u in self.owner.level.get_units_in_los(eye) if u != eye]
                if len(targets) > 0:
                    target = random.choice(targets)
                else:
                    continue
            target.apply_buff(EtherealnessBuff(), 3)

        enemy_targets = [u for u in self.owner.level.get_units_in_los(self.owner) if are_hostile(u, self.owner)]
        if len(enemy_targets) > 0:
            chosen_target = random.choice(enemy_targets)
        else:
            targets = [u for u in self.owner.level.get_units_in_los(self.owner) if u != self.owner]
            if len(targets) > 0:
                chosen_target = random.choice(targets)
            else:
                return
        chosen_target.apply_buff(EtherealnessBuff(), 3)
        
    def get_description(self):
        return ("Each turn you and your eye minions [ätherealies:äthereal] one unit in line of sight for 3 turns\n"
                "Prioretises enemies").format(**self.fmt_dict())
