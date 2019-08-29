import tcod
import tcod.event

from game_states import GameStates
from typing import Any

#FYI, keys are in tcod.event_constants, so use the next couple lines to grab the source code
#import inspect
#print(inspect(tcod.event_constants))


class Event_State_Manager:
    def __init__(self):
        self.play_state = Play_State()
        self.inv_state = Inv_State()
        self.dead_state = Dead_State()

        self.action = None
        self.mouse_pos = None

    def run_state(self, game_state, event):
        self.action = None
        if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            self.inv_state.dispatch(event)
            self.action = self.inv_state.action
        elif game_state == GameStates.PLAYER_DEAD:
            self.dead_state.dispatch(event)
            self.action = self.dead_state.action
        else:
            self.play_state.dispatch(event)
            self.action = self.play_state.action
            self.mouse_pos = self.play_state.mouse_pos


class Generic_State(tcod.event.EventDispatch):
    def __init__(self):
        self.action = None

    def dispatch(self, event: Any) -> None:
        self.action = None
        super().dispatch(event)

    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        key = event.sym

        if key == tcod.event.K_RETURN and ((tcod.event.KMOD_LALT | tcod.event.KMOD_RALT) & event.mod):
            self.action = {'fullscreen': True}
        elif key == tcod.event.K_ESCAPE:
            self.action = {'exit': True}


class Play_State(Generic_State):

    def __init__(self):
        self.mouse_pos = tcod.event.Point(0, 0)
        super().__init__()

    def ev_keydown(self, event):
        key = event.sym

        if key == tcod.event.K_k or key == tcod.event.K_UP:
            self.action = {'move': (0, -1)}
        elif key == tcod.event.K_j or key == tcod.event.K_DOWN:
            self.action = {'move': (0, 1)}
        elif key == tcod.event.K_h or key == tcod.event.K_LEFT:
            self.action = {'move': (-1, 0)}
        elif key == tcod.event.K_l or key == tcod.event.K_RIGHT:
            self.action = {'move': (1, 0)}
        elif key == tcod.event.K_y:
            self.action = {'move': (-1, -1)}
        elif key == tcod.event.K_u:
            self.action = {'move': (1, -1)}
        elif key == tcod.event.K_b:
            self.action = {'move': (-1, 1)}
        elif key == tcod.event.K_n:
            self.action = {'move': (1, 1)}
        elif key == tcod.event.K_PERIOD:
            self.action = {'rest': True}

        if key == tcod.event.K_g:
            self.action = {'pickup': True}
        elif key == tcod.event.K_i:
            self.action = {'show_inventory': True}
        elif key == tcod.event.K_d:
            self.action = {'drop_inventory': True}

        super().ev_keydown(event)

    def ev_mousemotion(self, event):
        self.action = None
        self.mouse_pos = event.tile


class Dead_State(Generic_State):
    def ev_keydown(self, event):
        key = event.sym

        if key == tcod.event.K_i:
            self.action = {'show_inventory': True}

        super().ev_keydown(event)


class Inv_State(Generic_State):
    def __init__(self):
        self.action = None
        self.mouse_pos = tcod.event.Point(0, 0)

    def ev_keydown(self, event):
        key = event.sym
        index = key - ord('a')

        if index >= 0:
            self.action = {'inventory_index': index}
        super().ev_keydown(event)
