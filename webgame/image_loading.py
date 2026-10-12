"""Load game images after the pygame display has been initialized."""
from types import SimpleNamespace

import pygame as pg

from config import *



"""Load and size the images and button rectangles used by the game."""
pond_original = pg.image.load(str(BASE_PATH / "assets/images/pond.png")).convert_alpha()
pond = pg.transform.scale(pond_original, (WIDTH, HEIGHT))
pond_rect = pond.get_rect()

# homescreen_original = pg.image.load("Homescreen.png").convert_alpha()
# homescreen = pg.transform.scale(homescreen_original, (WIDTH, HEIGHT))
# homescreen_rect = homescreen.get_rect()


homescreen_original = pg.image.load(str(BASE_PATH / "assets/images/menu_screen.png")).convert_alpha()
homescreen = pg.transform.scale(homescreen_original, (WIDTH, HEIGHT))
homescreen_rect = homescreen.get_rect()



levelscreen_original = pg.image.load(str(BASE_PATH / "assets/images/level_screen.png")).convert_alpha()
levelscreen = pg.transform.scale(levelscreen_original, (WIDTH, HEIGHT))
levelscreen_rect = levelscreen.get_rect()

title_original = pg.image.load(str(BASE_PATH / "assets/images/name_of_game.png")).convert_alpha()
title = pg.transform.scale(title_original, (250,200))
title_rect = title.get_rect()

frog_original = pg.image.load(str(BASE_PATH / "assets/images/frog.png")).convert_alpha()
frog = pg.transform.scale(frog_original, (frog_width,frog_width))
frog_rect = frog.get_rect()

lily_original = pg.image.load(str(BASE_PATH / "assets/images/lilypad.png")).convert_alpha()
lily = pg.transform.scale(lily_original, (lily_width, lily_height))
lily_rect = lily.get_rect()

indicator_original = pg.image.load(str(BASE_PATH / "assets/images/landing_indicator2.png")).convert_alpha()
visible_rect = indicator_original.get_bounding_rect()
indicator_original = indicator_original.subsurface(visible_rect).copy()
indicator = pg.transform.scale(indicator_original, (int(lily_width *indicator_scalar), int(lily_height*indicator_scalar)))
indicator_rect = indicator.get_rect()

arrow_original = pg.image.load(str(BASE_PATH / "assets/images/arrow.png")).convert_alpha()
arrow = pg.transform.scale(arrow_original, (100, 100))
arrow_loc = arrow.get_rect()
arrow_loc.center = 0.5*WIDTH/lily_count, HEIGHT*0.2

wooden_sign_original = pg.image.load(str(BASE_PATH / "assets/images/wooden_sign.png")).convert_alpha()
wooden_sign = pg.transform.scale(wooden_sign_original, (1000, 600))
wooden_sign_rect = wooden_sign.get_rect()
wooden_sign_rect.midtop = (640, -100)

menu_button_original = pg.image.load(str(BASE_PATH / "assets/images/menu_button.png")).convert_alpha()
menu_button = pg.transform.scale(menu_button_original, (250,126))
menu_button_rect = menu_button.get_rect()
menu_button_rect.topright = (1270,0)

undo_button_original = pg.image.load(str(BASE_PATH / "assets/images/clockwise-rotation.png")).convert_alpha()
undo_button = pg.transform.scale(undo_button_original, (60,60))
undo_button_rect = undo_button.get_rect()
undo_button_rect.topleft = (int(WIDTH*0.05), int(HEIGHT*0.05))

checkmark_original = pg.image.load(str(BASE_PATH / "assets/images/checkmark.png")).convert_alpha()
checkmark = pg.transform.scale(checkmark_original, (50, 50))
checkmark_rect = checkmark.get_rect()
