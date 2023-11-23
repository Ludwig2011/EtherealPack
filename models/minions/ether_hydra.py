from CommonContent import SimpleMeleeAttack
from Level import *
from mods.EtherealPack.models.minions.ether_breath import EtherBreath
from mods.EtherealPack.tags.Ethereal import Ethereal 

class EtherHydra(Unit):

	def __init__(self, elemental=False):
		super().__init__()
		self.sprite.char = 'D'
		self.sprite.color = Color(1,121,111)
		self.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
		self.name = "Äther Hydra"
		self.description = "Fires äther beams"
		self.max_hp = 45
		self.spells.append(EtherBreath(elemental))
		self.spells.append(SimpleMeleeAttack(9))
		self.resists[Ethereal] = 100
		self.resists[Tags.Physical] = 25
		self.resists[Tags.Arcane] = -50
		self.tags = [Tags.Dragon, Tags.Living, Ethereal]

	def get_ai_action(self):
		assert(not self.is_player_controlled)
		assert(self.is_alive())
		assert(not self.killed)

		# For now always channel if you can
		if self.has_buff(ChannelBuff):
			return PassAction()

		for spell in self.spells:
			if not spell.can_pay_costs():
				continue

			spell_target = spell.get_ai_target()
			if spell_target and not spell.can_cast(spell_target.x, spell_target.y):
				# Should not happen ever but sadly it does alot
				target_unit = self.level.get_unit_at(spell_target.x, spell_target.y)
				if target_unit:
					target_str = target_unit.name
					if target_unit == self:
						target_str = 'self'
				else:
					target_str = "empty tile"
				print("%s wants to cast %s on invalid target (%s)" % (self.name, spell.name, target_str))
				continue
			if spell_target:
				return CastAction(spell, spell_target.x, spell_target.y)

		possible_movement_targets = [u for u in self.level.units if self.level.are_hostile(self, u) and u.turns_to_death is None and self.can_harm(u)]

		# Non flying monsters will not move towards flyers over chasms
		if not self.flying:
			possible_movement_targets = [u for u in possible_movement_targets if self.level.tiles[u.x][u.y].can_walk]

		# The player is always prioritized if possible
		if any(u.is_player_controlled for u in possible_movement_targets):
			possible_movement_targets = [u for u in possible_movement_targets if u.is_player_controlled]

		if not possible_movement_targets:

			# Move randomly if there are no enemies in the level
			possible_movement_targets = [p for p in self.level.get_adjacent_points(Point(self.x, self.y), check_unit=True, filter_walkable=False) if self.level.can_stand(p.x, p.y, self)]
			if not possible_movement_targets:
				return PassAction()
			else:
				p = random.choice(possible_movement_targets)
				return MoveAction(p.x, p.y)

		target = min(possible_movement_targets, key = lambda t: distance(Point(self.x, self.y), Point(t.x, t.y)))

		if distance(Point(target.x, target.y), Point(self.x, self.y)) >= 2:
			path = self.find_path(self.level, Point(self.x, self.y), Point(target.x, target.y), self)

			if path:
				if libtcod.path_size(path) > 0:
					x, y = libtcod.path_get(path, 0)
					if self.level.can_move(self, x, y, force_swap=True):
						return MoveAction(x, y)

				libtcod.path_delete(path)

		return PassAction()

	def find_path(self, level, start, target, pather, pythonize=False, cosmetic=False):
		
		# Early out if the pather is surrounded by units and walls
		# If the unit cannot move, we dont care how it should move
		# Do not do this for cosmetic paths- they can step over units, and are infrequently called anyways
		if not cosmetic:
			boxed_in = True
			for p in level.get_adjacent_points(start, filter_walkable=False):
				unit = level.get_unit_at(p.x, p.y)
				if level.can_stand(p.x, p.y, pather) or (unit and not are_hostile(unit, self)):
					boxed_in = False
					break

			if boxed_in:
				return None

		def path_func(xFrom, yFrom, xTo, yTo, userData):
			tile = level.tiles[xTo][yTo]
			
			if pather.flying:
				if not tile.can_fly:
					return 0.0
			else:
				if not tile.can_walk:
					return 0.0
			 
			blocker_unit = tile.unit

			if not blocker_unit:
				if tile.prop:
					# player pathing avoids props unless prop is the target
					if (isinstance(tile.prop, Portal) or isinstance(tile.prop, Shop)) and pythonize and not (xTo == target.x and yTo == target.y):
						return 0.0
					# creatuers slight preference to avoid props
					return 1.1
				else:
					return 1.0
			if blocker_unit.stationary:
				return 1.0
			else:
				return 5.0


		path = libtcod.path_new_using_function(level.width, level.height, path_func)
		libtcod.path_compute(path, start.x, start.y, target.x, target.y)
		if pythonize:
			ppath = []
			for i in range(libtcod.path_size(path)):
				x, y = libtcod.path_get(path, i)
				ppath.append(Point(x, y))
			libtcod.path_delete(path)
			return ppath
		return path
	
	def advance(self, orders=None):
	
		can_act = True
		for b in self.buffs:
			if not b.on_attempt_advance():
				can_act = False

		if can_act:
			# Take an action
			if not self.is_player_controlled:
				action = self.get_ai_action()
			else:
				action = self.level.requested_action
				self.level.requested_action = None
				
			logging.debug("%s will %s" % (self, action))
			assert(action is not None)

			if isinstance(action, MoveAction):
				self.level.act_move(self, action.x, action.y, force_swap=True)
			elif isinstance(action, CastAction):
				self.level.act_cast(self, action.spell, action.x, action.y)
				if action.spell.quick_cast:
					return False
			elif isinstance(action, PassAction):
				self.level.event_manager.raise_event(EventOnPass(self), self)


		self.try_dismiss_ally()

		# TODO- post turn effects
		# TODO- return False if a non turn consuming action was taken
		return True