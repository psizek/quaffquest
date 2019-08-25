import tcod
import tcod.event

class State(tcod.event.EventDispatch):

    def __init__(self):
        self.action = None

    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        key = event.sym

        if key == tcod.event.K_ESCAPE:
            self.action = {'exit': True}

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


        if key == tcod.event.K_RETURN and ((tcod.event.KMOD_LALT | tcod.event.KMOD_RALT) & event.mod):
            self.action = {'fullscreen': True}
