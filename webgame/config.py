from pathlib import Path

import pygame as pg

from utils.helpers import set_frog_width
from utils.helpers import set_lily_height, set_lily_width


# Resolve all game files relative to the webgame folder.
BASE_PATH = Path(__file__).resolve().parent


#TODO fix music when playing in web game, because it does not work at the moment.
MUSIC = False

SIZE: tuple                 = (1280,720) #The display size of the screen. Currently cannot be changed.
WIDTH:int                   = SIZE[0]
HEIGHT:int                  = SIZE[1]
game_state: str             = "home" #game states are "home", "htp", "playing", "won"
lily_count: int             = 4 # Amount of lily's at the starting level
lily_width: int             = set_lily_width(lily_count, WIDTH)
lily_height: int            = set_lily_height()
frog_width: int             = set_frog_width()
arrow_index: int            = 2 # position of the selector
board: list[int]            = [1]*lily_count #Starting position of the frogs
board_history: list[tuple]  = [tuple(board)] #This memories all the previous states of the game at that level to enable undoing with z
arrow_rect: pg.Rect         = pg.Rect(0, 0, 100, 100) #dummy variable, later used for selector
is_selected: bool           = False #Has the player selected anything. Start of as False
indicator_scalar: float     = 1.4 #F stands for factor, which is the factor by which the indicator width and height are multiplied by the width and height of the lily
clicked: bool               = False #Is the mouse clicked. Used to prevent multiple clicks from being registered when the mouse is held down.
level_number: int           = 1 #The current level the player is on. Starts at 1.
is_music_on: bool           = True
main_channel                = None

LEVELS = {
    1:  (1,1,1,1),
    2:  (1,1,0,0,1,1),
    3:  (1,1,0,0,1,1,1),
    4:  (1,1,1,1,1),
    5:  (1,1,1,1,1,1),
    6:  (1,1,1,1,1,1,1),
    7:  (1,1,1,1,1,1,1,1),
    8:  (1,1,1,1,1,1,1,1,1),
    9:  (1,1,1,0,0,1,1,1,1,1),
    10: (1,1,1,1,1,1,1,1,1,1),
    11: (1,1,1,1,1,1,1,1,1,1,1),
    12: (2,1,1,2,2,1,0,2),
    13: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    14: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    15: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    16: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    17: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    18: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    19: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
    20: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
}