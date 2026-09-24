"""
Created by Edwin Ma. Check out my GitHub at: 
"""

import asyncio
import pygame as pg
from pygame import mixer

import os
import math

from button import Button
from htp import HowToPlay
from levels import LEVELS

#PART 1: Define functions
def player_has_won(board_state:list) -> bool:
    """Returns True if the player has won the game, False otherwise. The player wins if all frogs are on the same lilypad."""
    return max(board_state) == sum(board_state)


def get_jump_distance(frog_count:int) -> int:
    """Returns the distance a frog can jump based on the number of frogs on the lilypad. The distance is 2*frog_count - 1. If there are no frogs, the distance is 0."""
    if frog_count == 0:
        return 0
    else:
        return 2*frog_count -1

def get_landing_index(arrow_index:int, frog_count:int, direction:str) -> int:
    """Returns the index of the lilypad the frog will land on"""
    distance = get_jump_distance(frog_count)

    if direction == "left":
        return arrow_index -distance
    elif direction == "right":
        return arrow_index + distance

def is_valid_landing(landing_index:int, board:list = []) -> bool:
    """Returns True if the landing index is valid, False otherwise. A landing index is valid if it is within the bounds of the board and there is at least one frog on the lilypad."""
    if landing_index >=0 and landing_index <len(board) and board[landing_index] > 0:
        return True
    else:
        return False

def draw_lilypads(screen:tuple, width:int, height:int, image, lilypad_count:int) -> int:
    """Draws the lilypads on the screen. The lilypads are evenly spaced across the width of the screen."""
    for i in range(0,lilypad_count):
        lilypad_rect = image.get_rect()
        lilypad_rect.center = ((i+0.5)*width//lilypad_count, int(0.8*height))

        dummy = None
        if Button(image, lilypad_rect).draw(screen):
            dummy = i
    return dummy

def draw_arrow(screen, width, height, image, arrow_index, lilypad_count, is_selected):
    """Draws the arrow on the screen."""
    arrow_rect = image.get_rect()
    arrow_rect.center = ((arrow_index+0.5)*width/lilypad_count, 0.3*height+is_selected*0.1*height)
    screen.blit(image, arrow_rect)

def set_lilypad_width(lilypad_count:int, width:int) -> int:
    """Returns the width of the lilypad based on the number of lilypads and the width of the screen. 
    The width is set to be the minimum of the width of the screen divided by the number of lilypads minus 10 and 200. 
    This ensures that the lilypads are not too small or too large."""
    return int(min(width/lilypad_count - 10, 200))

def set_lilypad_height() -> int:
    """Returns the height of the lilypad. The height is set to be 70 pixels for now."""
    return 70

def set_frog_width(lilypad_count:int = 4, WIDTH  = 1280) -> int:
    """Returns the width of the frog. The width is set to be 102 pixels for now."""
    return int(min(102, WIDTH/lilypad_count - 10))

def set_frog_height(frog_width:int = 102) -> int:
    """Returns the height of the frog. The height is set to be 70 pixels for now."""
    return int(frog_width * 70 / 102)

def get_level_rects() -> list:
    """Returns a list of pygame.Rect objects representing the clickable areas for each level button on the level selection screen."""
    level_rects = []
    start_x = 330
    start_y = 222
    spacing_x = 127
    spacing_y = 94
    button_width = 116
    button_height = 82

    for row in range(4):
        for col in range(5):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            rect = pg.Rect(
                x,
                y,
                button_width,
                button_height
            )

            level_rects.append(rect)
    return level_rects

# async is needed for webapp
async def main():

    SIZE: tuple             = (1280,720) #The display size of the screen. Currently cannot be changed.
    WIDTH:int               = SIZE[0]
    HEIGHT:int              = SIZE[1]
    game_state: str         = "home" #game states are "home", "htp", "playing", "won"
    lilypad_count: int      = 4 # Amount of lilypad at the starting level
    lilypad_width: int      = set_lilypad_width(lilypad_count, WIDTH)
    lilypad_height: int     = set_lilypad_height()
    frog_width: int         = set_frog_width()
    arrow_index: int        = 2 # position of the selector
    board: [int]            = [1]*lilypad_count #Starting position of the frogs
    board_history: [tuple]  = [tuple(board)] #This memories all the previous states of the game at that level to enable undoing with z
    arrow_rect: pg.Rect     = pg.Rect(0, 0, 100, 100) #dummy variable, later used for selector
    is_selected: bool       = False #Has the player selected anything. Start of as False
    indicator_scalar: float = 1.4 #F stands for factor, which is the factor by which the indicator width and height are multiplied by the width and height of the lilypad
    clicked: bool           = False #Is the mouse clicked. Used to prevent multiple clicks from being registered when the mouse is held down.
    level_number: int      = 1 #The current level the player is on. Starts at 1.

    #initialize Pygame
    pg.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Jumping Frogs")
    clock = pg.time.Clock()
    my_font = pg.font.SysFont("Comic Sans MS", 30)
    
    #apply changes
    pg.display.update()


    def start_level(level_number:int, starting_board:tuple) ->None:

        nonlocal lilypad_count
        nonlocal lilypad_width
        nonlocal lilypad_rect
        nonlocal lilypad
        nonlocal indicator
        nonlocal indicator_rect
        nonlocal board
        nonlocal board_history
        nonlocal arrow_index
        nonlocal is_selected
        nonlocal game_state


        lilypad_count = len(starting_board)

        board_history = [starting_board]
        board = list(starting_board)
        

        arrow_index = lilypad_count // 2
        is_selected = False
        game_state = "playing"

        lilypad_width = set_lilypad_width(lilypad_count, WIDTH)
        lilypad_height = set_lilypad_height()
        lilypad_rect = pg.Rect(0,0,lilypad_width, lilypad_height)
        lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
        indicator = pg.transform.scale(indicator_original, (int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar)))
        indicator_rect = pg.Rect(0,0,int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar))

    level_rects = get_level_rects()
    level_to_home_button_rect = pg.Rect(1045, 605, 206, 74)

    #PART 2: load images
    screen_rect = pg.Rect(0,0,WIDTH, HEIGHT)

    pond_original = pg.image.load("pond.png").convert_alpha()
    pond = pg.transform.scale(pond_original, (WIDTH, HEIGHT))
    pond_rect = pond.get_rect()

    # homescreen_original = pg.image.load("Homescreen.png").convert_alpha()
    # homescreen = pg.transform.scale(homescreen_original, (WIDTH, HEIGHT))
    # homescreen_rect = homescreen.get_rect()


    homescreen_original = pg.image.load("ChatGPT Image Sep 22, 2026, 12_41_36 PM.png").convert_alpha()
    homescreen = pg.transform.scale(homescreen_original, (WIDTH, HEIGHT))
    homescreen_rect = homescreen.get_rect()



    levelscreen_original = pg.image.load("level_screen.png").convert_alpha()
    levelscreen = pg.transform.scale(levelscreen_original, (WIDTH, HEIGHT))
    levelscreen_rect = levelscreen.get_rect()

    title_original = pg.image.load("name_of_game.png").convert_alpha()
    title = pg.transform.scale(title_original, (250,200))
    title_rect = title.get_rect()

    frog_original = pg.image.load("frog.png").convert_alpha()
    frog = pg.transform.scale(frog_original, (frog_width,frog_width))
    frog_rect = frog.get_rect()

    Lilypad_original = pg.image.load("lilypad.png").convert_alpha()
    lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
    lilypad_rect = lilypad.get_rect()

    indicator_original = pg.image.load("landing_indicator2.png").convert_alpha()
    visible_rect = indicator_original.get_bounding_rect()
    indicator_original = indicator_original.subsurface(visible_rect).copy()
    indicator = pg.transform.scale(indicator_original, (int(lilypad_width *indicator_scalar), int(lilypad_height*indicator_scalar)))
    indicator_rect = indicator.get_rect()

    arrow_original = pg.image.load("arrow.png").convert_alpha()
    arrow = pg.transform.scale(arrow_original, (100, 100))
    arrow_loc = arrow.get_rect()
    arrow_loc.center = 0.5*WIDTH/lilypad_count, HEIGHT*0.2

    wooden_sign_original = pg.image.load("wooden_sign.png").convert_alpha()
    wooden_sign = pg.transform.scale(wooden_sign_original, (1000, 600))
    wooden_sign_rect = wooden_sign.get_rect()
    wooden_sign_rect.midtop = (640, -100)

    menu_button_original = pg.image.load("menu_button.png").convert_alpha()
    menu_button = pg.transform.scale(menu_button_original, (250,126))
    menu_button_rect = menu_button.get_rect()
    menu_button_rect.topright = (1270,0)

    #DRAW rectangles over play-button, How-to-Play button on the home screen.
    play_button_rect = pg.Rect(472, 332, 343, 90)
    htp_button_rect = pg.Rect(472, 447, 343, 77)
    levels_button_rect = pg.Rect(472,554, 343, 77)




    # Tutorial owns its page number and example; it never changes the real board.
    tutorial = HowToPlay(pond, frog_original, Lilypad_original)

    #PART 3: Main loop
    running = True
    while running:
        clock.tick(60) #Set frame-rate to 60 fps
        pos = pg.mouse.get_pos() #pos is the position of the mouse on the game-screen
        #event handler
        for event in pg.event.get():
            #If user quits the game, the game quits in order to exit the while loop.
            if event.type == pg.QUIT:
                running = False

            if game_state == "htp":
                next_state = tutorial.handle_event(event)
                if next_state is not None:
                    game_state = next_state
                # Do not let tutorial navigation also trigger gameplay controls.
                continue

            elif game_state == "levels": #Player is at the levels-screen
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        for index, rect in enumerate(level_rects):

                            if rect.collidepoint(event.pos):

                                level_number = index + 1

                                print("Selected level:", level_number)
                                start_level(level_number, LEVELS[level_number])
                                
                        if level_to_home_button_rect.collidepoint(pos):
                            game_state = "home"

            elif game_state == "won":
                if event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    level_number += 1
                    if level_number in LEVELS:
                        start_level(level_number, LEVELS[level_number])
                        game_state = "playing"
                    else:
                        screen.fill("light blue")
                        text_surface = my_font.render("You have completed all levels! Press any key to return to the home screen.", False, (0, 0, 0))
                        screen.blit(text_surface, (100, 300))
                        pg.display.update()
                        waiting_for_key = True
                        while waiting_for_key:
                            for event in pg.event.get():
                                if event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                                    waiting_for_key = False
                                    game_state = "home"
    
                    

            elif game_state == "playing":

                #All the mouse controls for the game are handled here.
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for i, rect in enumerate(lilypad_rects):
                            if rect.collidepoint(event.pos):
                                if is_selected == False and board[i] != 0:
                                    arrow_index = i
                                    is_selected = True
                                elif is_selected == True and i in [get_landing_index(arrow_index, board[arrow_index], "left"), get_landing_index(arrow_index, board[arrow_index], "right")] and is_valid_landing(i, board):
                                    board[i] += board[arrow_index]
                                    board[arrow_index] = 0
                                    arrow_index = i
                                    is_selected = False
                                    board_history.append(tuple(board))


                #All the keyboard controls for the game are handled here.
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_a, pg.K_LEFT] and is_selected == False:
                        if arrow_index != 0:
                            arrow_index = arrow_index -1
                            arrow_rect.move_ip(-(WIDTH/lilypad_count), 0)
                    elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == False:
                        if arrow_index != lilypad_count -1:
                            arrow_index = arrow_index +1
                    elif event.key in [pg.K_s, pg.K_DOWN] and board[arrow_index]!=0:
                        is_selected = True
                    elif event.key in [pg.K_w, pg.K_UP]:
                        is_selected = False

                    elif event.key in [pg.K_a, pg.K_LEFT] and is_selected == True:
                        landing_index = get_landing_index(arrow_index, board[arrow_index],"left")
                        if is_valid_landing(landing_index, board) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(tuple(board))

                    elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == True:
                        landing_index = get_landing_index(arrow_index, board[arrow_index],"right")
                        if is_valid_landing(landing_index, board) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(tuple(board))
                            
                    #r is restart
                    elif event.key in [pg.K_r]:
                        board = [1]*lilypad_count
                        board_history = [tuple(board)]
                        is_selected = False
                        arrow_index = math.ceil(lilypad_count/2) -1

                    #z is undo
                    elif event.key in [pg.K_z] and len(board_history) >1:
                        board_history.pop()
                        board = list(board_history[-1])
                        is_selected = False
                        arrow_index = math.ceil(lilypad_count/2) -1

                    #m returns to menu
                    elif event.key in [pg.K_m]:
                        game_state = "home"
                        is_selected = False
                        arrow_index = math.ceil(lilypad_count/2) -1
                        

        #Drawing part of the loop
        if game_state == "home":
            
            #check mouseover and clicked conditions
            if play_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "playing"
            elif htp_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    tutorial.reset()
                    game_state = "htp"
            elif levels_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "levels"

            if pg.mouse.get_pressed()[0] == 0:
                clicked = False

            screen.blit(homescreen, homescreen_rect)

        elif game_state == "htp":
            tutorial.draw(screen)

        elif game_state == "levels":
            screen.blit(levelscreen, levelscreen_rect)

            # for i in range(0,len(level_rects)):
            #     pg.draw.rect(screen, "red", level_rects[i], 3)

            # pg.draw.rect(screen, "red", level_to_home_button_rect, 3)

            for rect in level_rects:

                if rect.collidepoint(pos):

                    pg.draw.ellipse(
                        screen,
                        (255, 255, 100),
                        rect,
                        4
                    )

        if game_state == "playing" or game_state == "won":

            #Fill background
            screen.blit(pond, pond_rect)

            #Menu button
            screen.blit(menu_button, menu_button_rect)

            if menu_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "home"
            if pg.mouse.get_pressed()[0] == 0:
                clicked = False

            #Draw the water ripples.
            if is_selected == True:
                indicator_left = get_landing_index(arrow_index, board[arrow_index], "left")
                indicator_right = get_landing_index(arrow_index, board[arrow_index], "right")
                if is_valid_landing(indicator_left, board):
                    indicator_rect.center = ((indicator_left + 0.5) * WIDTH//lilypad_count, int(0.8*HEIGHT))
                    screen.blit(indicator, indicator_rect)
                if is_valid_landing(indicator_right, board):
                    indicator_rect.center = ((indicator_right + 0.5)*WIDTH//lilypad_count, int(0.8*HEIGHT))
                    screen.blit(indicator,indicator_rect)

            #Draw the lilypads
            lilypad_rects = []
            for i in range(0, lilypad_count):
                lilypad_rect = lilypad.get_rect()
                lilypad_rect.center = ((i + 0.5)*WIDTH//lilypad_count, int(0.8*HEIGHT))
                screen.blit(lilypad, lilypad_rect)
                lilypad_rects.append(lilypad_rect)

            #Draw an ellipse around the lilypad the mouse is hovering over.
            for rect in lilypad_rects:
                if rect.collidepoint(pos):
                    pg.draw.ellipse(
                        screen,
                        (255, 255, 100),
                        rect,
                        4
                    )

            #Draw arrow above
            draw_arrow(screen, WIDTH, HEIGHT, arrow, arrow_index, lilypad_count, is_selected)

            #Draw the frogs
            if lilypad_count <= 10:
                frog_stack_spacing = int(0.5*frog_width)
            else:
                 frog_stack_spacing = int(0.42*frog_width)
            for i in range(0, lilypad_count):
                for ii in range(board[i]-1, -1, -1):
                    frog_rect.midbottom = ((i + 0.5)*WIDTH/lilypad_count, 0.8*HEIGHT-(frog_stack_spacing*ii))
                    screen.blit(frog, frog_rect)

            if player_has_won(board) and game_state == "playing":
                game_state = "won"
                continue
                
        if game_state == "won":
            screen.blit(wooden_sign, wooden_sign_rect)
            text_surface1 = my_font.render("Congrats! You win level "+ str(level_number) + "!", False, (0, 0, 0))
            text_surface2 = my_font.render("Press any key to continue to level  "+ str(level_number + 1) + ".", False, (0, 0, 0))
            
            screen.blit(text_surface1, (434, 123))
            screen.blit(text_surface2, (434, 232))


        if pg.mouse.get_pressed()[0] == 1 and clicked == False:
            clicked = True
            print(pos)

        if pg.mouse.get_pressed()[0] == 0:
            clicked = False      

            
    

        await asyncio.sleep(0)

        pg.display.update()
    pg.quit()
asyncio.run(main())