import tcod
import tcod.event

class State(tcod.event.EventDispatch):
    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        if event.sym == 'j':

