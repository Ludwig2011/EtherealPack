import ModHandler
from Level import Color, EventOnUnitAdded, Level, Tag, Tags, Upgrade
#TODO make euqipment staff that gives bonus charges and duration
#TODO make icons animated again!
#TODO fix level clear plus hazard remove chasms!?
#TODO ethermancer trial give ethermancer robe
#TODO make offmap spells use same helper for unit copy etc
#TODO fix description color and variables in spells/equipment
#TODO make spells/equipment scale with appropiate spell bonuses where not already done. Mostly missing for upgrades / equipment
#TODO Rename skill folder to equipment and make sure imports etc dont break 
Ethereal = ModHandler.register_tag("Äthereal", Color(1, 255, 188), letter="v", asset=["EtherealPack", "ether"])
Etherealness = Tag("Ätherealness", Color(1, 255, 188))


def on_unit_added(evt):
    unit = evt.unit

    if Tags.Arcane in unit.tags:
        unit.resists[Ethereal] += 25

        if unit.max_hp > 29:
            unit.resists[Ethereal] += 25

            if unit.max_hp > 99:
                unit.resists[Ethereal] += 25

    if Tags.Holy in unit.tags or Tags.Dark in unit.tags:
        unit.resists[Ethereal] -= 50


# Preserve the original initializer.
_original_level_init = Level.__init__


def level_init_with_ethereal_rules(self, w, h):
    # Initialize the level normally, including its event manager.
    _original_level_init(self, w, h)

    # Register the rules for this level.
    self.event_manager.register_global_trigger(
        EventOnUnitAdded,
        on_unit_added
    )


# Replace the initializer.
Level.__init__ = level_init_with_ethereal_rules