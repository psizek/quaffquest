from typing import Dict
from tcod import Color


WINDOW_TITLE: str = 'Quaff Quest'

SCREEN_WIDTH: int = 80
SCREEN_HEIGHT: int = 50

BAR_WIDTH: int = 20
PANEL_HEIGHT: int = 7
PANEL_Y: int = SCREEN_HEIGHT - PANEL_HEIGHT

MESSAGE_X: int = BAR_WIDTH + 2
MESSAGE_WIDTH: int = SCREEN_WIDTH - BAR_WIDTH - 2
MESSAGE_HEIGHT: int = PANEL_HEIGHT - 1

MAP_WIDTH: int = 80
MAP_HEIGHT: int = 43

ROOM_MAX_SIZE: int = 10
ROOM_MIN_SIZE: int = 6
MAX_ROOMS: int = 30

FOV_ALGORITHM: int = 0
FOV_LIGHT_WALLS: bool = True
FOV_RADIUS: int = 10

COLORS: Dict[str, Color] = {
    'dark_wall': Color(0, 0, 100),
    'dark_ground': Color(50, 50, 150),
    'light_wall': Color(130, 110, 50),
    'light_ground': Color(200, 180, 50)
}
