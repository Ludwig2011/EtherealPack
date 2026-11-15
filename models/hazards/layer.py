import sys

import Level


_original_iter_frame = Level.Level.iter_frame


def advance_hazards(level):
    for hazard in list(getattr(level, "hazards", ())):
        hazard.advance()
    while level.can_advance_spells():
        yield level.advance_spells()


def is_turn_end(iterator):
    while iterator is not None:
        code = getattr(iterator, "gi_code", None)
        if code is not None and code.co_name == "iter_frame" and iterator.gi_yieldfrom is None:
            return True
        iterator = getattr(iterator, "gi_yieldfrom", None)
    return False


def iter_frame_with_hazards(self):
    previous_turn = self.turn_no
    has_completed_turn = False

    iterator = _original_iter_frame(self)
    while True:
        try:
            result = next(iterator)
        except StopIteration:
            return

        if result is True and is_turn_end(iterator):
            yield from advance_hazards(self)
            previous_turn = self.turn_no
            has_completed_turn = True
        elif Level.visual_mode and self.turn_no > previous_turn:
            if has_completed_turn:
                yield from advance_hazards(self)
            previous_turn = self.turn_no
            has_completed_turn = True
        yield result


Level.Level.iter_frame = iter_frame_with_hazards


PyGameView = sys.modules["__main__"].PyGameView
_original_draw_level = PyGameView.draw_level
_original_draw_prop = PyGameView.draw_prop


def draw_prop_with_hazards(self, prop, *args, **kwargs):
    draw_levels = getattr(self, "_ethereal_hazard_draw_levels", None)
    if draw_levels is None:
        return _original_draw_prop(self, prop, *args, **kwargs)

    drawn_hazards = self._ethereal_drawn_hazards
    if id(prop) in drawn_hazards:
        return

    result = _original_draw_prop(self, prop, *args, **kwargs)
    for level in draw_levels:
        if not (0 <= prop.x < level.width and 0 <= prop.y < level.height):
            continue
        tile = level.tiles[prop.x][prop.y]
        hazards = getattr(tile, "hazards", ())
        if prop is not tile.prop and prop not in level.props:
            continue

        if any(hazard is prop for hazard in hazards):
            drawn_hazards.add(id(prop))
        for hazard in hazards:
            if id(hazard) in drawn_hazards:
                continue
            _original_draw_prop(self, hazard, *args, **kwargs)
            drawn_hazards.add(id(hazard))
        break

    return result


def draw_level_with_hazards(self):
    levels = []
    seen = set()
    for level in (
        getattr(self.game, "cur_level", None),
        getattr(self.game, "next_level", None),
        getattr(self.game, "prev_next_level", None),
    ):
        if level is None or id(level) in seen:
            continue
        seen.add(id(level))
        levels.append(level)

    appended_props = []
    replaced_tile_props = []
    self._ethereal_hazard_draw_levels = levels
    self._ethereal_drawn_hazards = set()
    try:
        for level in levels:
            for hazard in getattr(level, "hazards", ()):
                if hazard not in level.props:
                    level.props.append(hazard)
                    appended_props.append((level, hazard))

                tile = level.tiles[hazard.x][hazard.y]
                if tile.prop is None:
                    tile.prop = hazard
                    replaced_tile_props.append((tile, hazard))

        return _original_draw_level(self)
    finally:
        for tile, hazard in replaced_tile_props:
            if tile.prop is hazard:
                tile.prop = None
        for level, hazard in appended_props:
            if hazard in level.props:
                level.props.remove(hazard)
        del self._ethereal_hazard_draw_levels
        del self._ethereal_drawn_hazards


PyGameView.draw_prop = draw_prop_with_hazards
PyGameView.draw_level = draw_level_with_hazards
