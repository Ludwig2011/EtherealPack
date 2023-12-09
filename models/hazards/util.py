import copy
from Level import *

def get_hazard_point(level, x, y, radius_limit=25, sort_dist=True, flying=False, diag=False):
		options = list(level.get_points_in_ball(x, y, radius_limit, diag=diag))
		random.shuffle(options)
		
		if sort_dist:
			options.sort(key=lambda p: distance(p, Point(x, y)))

		for o in options:
			tile = level.tiles[o.x][o.y]
			if not flying:
				if not tile.can_walk:
					continue
			else:
				if not tile.can_fly:
					continue
			if not tile.prop == None:
				continue
			return o

		return None

def deal_damage(level, unit, amount, damage_type, source):
    # Raise pre damage event (for conversions)
    pre_damage_event = EventOnPreDamaged(unit, amount, damage_type, source)
    level.event_manager.raise_event(pre_damage_event, unit)

    # Factor in shields and resistances after raising the raw pre damage event
    resist_amount = unit.resists.get(damage_type, 0)

    # Cap effective resists at 100- shenanigans ensue if we do not
    resist_amount = min(resist_amount, 100)

    if resist_amount:
        multiplier = (100 - resist_amount) / 100.0
        amount = int(math.ceil(amount * multiplier))

    if amount > 0 and unit.shields > 0:
        unit.shields = unit.shields - 1
        level.combat_log.debug("%s blocked %d %s damage from %s" % (unit.name, amount, damage_type.name, source.name))
        level.show_effect(unit.x, unit.y, Tags.Shield_Expire)				
        return False

    amount = min(amount, unit.cur_hp)
    unit.cur_hp = unit.cur_hp - amount

    if amount > 0:
        level.combat_log.debug("%s took %d %s damage from %s" % (unit.name, amount, damage_type.name, source.name))
    elif amount < 0:
        level.combat_log.debug("%s healed %d from %s" % (unit.name, -amount, source.name))

    if (amount > 0):

        # Record damage for post level summary
        if source.owner and source.owner != level.player_unit:
            source_key = "%s (%s)" % (source.name, source.owner.name)
            level.damage_taken_sources
        else:
            source_key = "%s" % source.name

        # Record damage sources when a player unit exists (aka not in unittests)
        if level.player_unit:
            if are_hostile(unit, level.player_unit):
                key = source.name
                if source.owner and source.owner.source:
                    key = source.owner.name

                level.damage_dealt_sources[key] += amount
            elif unit == level.player_unit:
                if source.owner:
                    key = source.owner.name
                else:
                    key = source.name	
                level.damage_taken_sources[key] += amount
    
        if (unit.cur_hp <= 0):
            if not unit.killed:
                unit.cur_hp = 0
                unit.killed = True
                damage_event = EventOnDamaged(unit, amount, damage_type, source)
                level.event_manager.raise_event(damage_event, unit)
                for buff in unit.buffs:
                    buff.unapply()
                unit.level.event_manager.raise_event(EventOnDeath(unit, damage_event), unit)

            if (unit.cur_hp <= 0):
                if not unit.killed:
                    unit.cur_hp = 0
                    unit.killed = True
                    damage_event = EventOnDamaged(unit, amount, damage_type, source)
                    level.event_manager.raise_event(damage_event, unit)
                    for buff in unit.buffs:
                        buff.unapply()
                    unit.level.event_manager.raise_event(EventOnDeath(unit, damage_event), unit)	

            return True
        else:
            damage_event = EventOnDamaged(unit, amount, damage_type, source)
            level.event_manager.raise_event(damage_event, unit)

        if (unit.cur_hp > unit.max_hp):
            unit.cur_hp = unit.max_hp
    # set amount to 0 if there is no unit- ie, if an empty tile or dead unit was hit
    else:
        amount = 0

    if (unit.cur_hp > unit.max_hp):
        unit.cur_hp = unit.max_hp

    return False

def add_unit(level, unit, x, y, unit_buffs, trigger_summon_event=True):
            unit.x = x
            unit.y = y
            unit.level = level

            if not hasattr(unit, 'level_id'):
                unit.level_id = level.level_id

            if trigger_summon_event:
                level.event_manager.raise_event(EventOnUnitPreAdded(unit), unit)
                
            assert(level.tiles[x][y].unit is None)
            level.tiles[x][y].unit = unit

            # Hack- allow improper adding in monsters.py
            for spell in unit.spells:
                spell.caster = unit
                spell.owner = unit
                    
            level.units.append(unit)
            if trigger_summon_event:
                level.event_manager.raise_event(EventOnUnitAdded(unit), unit)

            unit.ever_spawned = True
