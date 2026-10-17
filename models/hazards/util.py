import copy
from Level import *

def suspend_unit_events(unit):
    if getattr(unit, '_stasis_events_suspended', False): return
    for buff in unit.buffs:
        if buff.applied: buff.unsubscribe()
    unit._stasis_events_suspended = True

def resume_unit_events(unit):
    if not getattr(unit, '_stasis_events_suspended', False): return
    unit._stasis_events_suspended = False
    for buff in unit.buffs:
        if buff.applied: buff.subscribe()

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

def deal_off_grid_damage(level, unit, amount, damage_type, source):
    """Damage a unit held off-grid in stasis without firing position-dependent callbacks."""
    if unit in level.units:
        raise ValueError("off-grid stasis damage requires a detached unit")
    suspend_unit_events(unit)

    if amount == 0:
        return False

    if amount > 0:
        damage_state = (unit, unit.cur_hp, unit.shields)
        damage_instance_count = level.damage_instances.get(damage_state, 0)
        if damage_instance_count >= DAMAGE_INSTANCE_CAP:
            return False
        level.damage_instances[damage_state] = damage_instance_count + 1

    resist_amount = min(unit.resists.get(damage_type, 0), 100)
    amount = int(math.ceil(amount * (100 - resist_amount) / 100.0))

    if amount > 0 and unit.shields > 0:
        unit.shields -= 1
        level.log("%s blocked %d %s damage from %s" % (unit.name, amount, damage_type.name, source.name))
        return False

    if amount > 0:
        amount = min(amount, unit.cur_hp)
        if unit.damage_floors:
            amount = min(amount, max(0, unit.cur_hp - unit.damage_floors[-1][1]))
            if amount <= 0:
                return False
    elif amount < 0:
        amount = max(amount, unit.cur_hp - unit.max_hp)

    unit.cur_hp -= amount
    if amount > 0:
        level.log("%s took %d %s damage from %s" % (unit.name, amount, damage_type.name, source.name))
    elif amount < 0:
        level.log("%s healed %d from %s" % (unit.name, -amount, source.name))

    if amount <= 0:
        return False
    if level.player_unit:
        if are_hostile(unit, level.player_unit):
            key = source.name
            if source.owner and source.owner.source:
                key = source.owner.name
            level.damage_dealt_sources[key] += amount
            level.turn_summary.damage_dealt[key] += amount
        elif unit == level.player_unit:
            key = source.owner.name if source.owner else source.name
            level.damage_taken_sources[key] += amount
            level.turn_summary.self_damage_taken[key] += amount
        else:
            if isinstance(source, Buff) and source.buff_type == BUFF_TYPE_CURSE:
                key = source.name
            elif source.owner:
                key = source.owner.name
            else:
                key = source.name
            level.turn_summary.ally_damage_taken[key] += amount

    if unit.cur_hp > 0 or unit.killed:
        return False
    unit.cur_hp = 0
    if level.player_unit and level.player_unit != unit:
        if are_hostile(level.player_unit, unit):
            level.turn_summary.enemy_kill_counts[unit.name] += 1
        else:
            level.turn_summary.ally_kill_counts[unit.name] += 1
    unit.killed = True
    for buff in list(unit.buffs):
        if buff.applied:
            buff.unsubscribe()
            buff.applied = False
    unit.buffs.clear()
    return True

def add_unit(level, unit, x, y, unit_buffs, trigger_summon_event=True):
            unit.x = x
            unit.y = y
            unit.level = level

            resume_unit_events(unit)

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
