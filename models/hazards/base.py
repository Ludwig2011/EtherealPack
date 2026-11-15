from Level import Prop


class EtherealHazard(Prop):
    def __init__(self, name, duration, user):
        self.name = name
        self.duration = duration
        self.user = user

    def on_unit_enter(self, unit):
        self.effect(unit)

    def effect(self, unit):
        pass

    def advance(self):
        self.advance_effect()
        self.duration -= 1
        if self.duration <= 0:
            self.level.remove_hazard(self)

    def advance_effect(self):
        pass

    def get_description(self):
        return "%d turns remaining" % self.duration
