import pygame as pg

from image_loading import *
from utils.helpers import draw_speaker



play_button_rect = pg.Rect(472, 332, 343, 90)
htp_button_rect = pg.Rect(472, 447, 343, 77)
levels_button_rect = pg.Rect(472,554, 343, 77)


def draw_menu(screen, is_music_on):
    screen.blit(homescreen, homescreen_rect)
    draw_speaker(screen, speaker_on, speaker_off, speaker_rect, is_music_on)



def handle_menu_input(event):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if play_button_rect.collidepoint(event.pos):
            return "playing"
        elif htp_button_rect.collidepoint(event.pos):
            return "htp"
        elif levels_button_rect.collidepoint(event.pos):
            return "levels"

    return "home"