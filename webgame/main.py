"""
Created by Edwin Ma. Check out my GitHub at: https://github.com/edwinzma
"""
import sys
import math
import config
import scene
from enum import Enum


import asyncio
import pygame as pg

from config import *
from scene import Scene

# Initialize only the display and fonts; the game has no audio.
pg.display.init()
pg.font.init()
in_browser = sys.platform == "emscripten"

screen = pg.display.set_mode(SIZE)
pg.display.set_caption("Jumping Frogs")
clock = pg.time.Clock()
my_font = pg.font.SysFont("Comic Sans MS", 30)


from scenes.htp import HowToPlay
from image_loading import *
from utils.helpers import *
from scenes.menu import *


# async is needed for webapp
async def main() -> None:
    global lily_count, lily_width, crown_history
    crown_index = config.crown_index
    # Initialize state here because assignments below make these variables local.
    level_number = config.level_number
    board = list(config.board)
    board_history = list(config.board_history)
    arrow_index = config.arrow_index
    is_selected = config.is_selected
    game_state = scene.game_state
    trampoline_indexes = LEVELS[level_number].get("trampoline_indexes", ())

    #apply changes
    pg.display.update()

    #set rects
    level_rects = get_level_rectangles()
    level_to_home_button_rect = pg.Rect(1045, 605, 206, 74)
    screen_rect = pg.Rect(0,0,WIDTH, HEIGHT)

    # Tutorial owns its page number and example; it never changes the real board.
    tutorial = HowToPlay(pond, frog_original, lily_original)

    # Prepare graphics for every board size.
    level_graphics = {}
    for count in sorted({lily_count} | {len(dictionary["board"]) for dictionary in LEVELS.values()}):
        pad_width = set_lily_width(count, WIDTH)
        pad = pg.transform.scale(lily_original, (pad_width, lily_height))
        ripple = pg.transform.scale(
            indicator_original,
            (int(pad_width * indicator_scalar), int(lily_height * indicator_scalar))
        )
        rects = []
        for i in range(count):
            rect = pad.get_rect()
            rect.center = ((i + 0.5) * WIDTH // count, int(0.8 * HEIGHT))
            rects.append(rect)
        level_graphics[count] = (pad, ripple, rects)
        await asyncio.sleep(0)
    lily, indicator, lily_rects = level_graphics[lily_count]
    lily_rect = lily.get_rect()
    indicator_rect = indicator.get_rect()

    # Text rendering is done once, not on each frame of the win screen.
    win_text = {}
    for number in sorted(set(LEVELS) | {level_number}):
        win_text[number] = (
            my_font.render("Congrats! You win level " + str(number) + "!", False, (0, 0, 0)),
            my_font.render("Press any key to continue to level  " + str(number + 1) + ".", False, (0, 0, 0))
        )
        await asyncio.sleep(0)
    completed_text = my_font.render(
        "You have completed all levels! Press any key to return to the home screen.",
        False, (0, 0, 0)
    )

    
    #Main loop
    running = True
    while running:
        # Let Pygbag/browser schedule frames instead of blocking in tick(60).
        # Desktop still uses the original 60 FPS limit.
        if not in_browser:
            clock.tick(60)
        pos = pg.mouse.get_pos() #pos is the position of the mouse on the game-screen

        #event handler
        for event in pg.event.get():
            #If user quits the game, the game quits in order to exit the while loop.
            if event.type == pg.QUIT:
                running = False
                break

            
            if game_state == Scene.HOME:
                game_state = handle_menu_input(event)
                if game_state == Scene.HOWTOPLAY:
                    tutorial.reset()

            elif game_state == Scene.HOWTOPLAY:
                next_state = tutorial.handle_event(event)
                if next_state is not None:
                    game_state = next_state
                # Do not let tutorial navigation also trigger gameplay controls.
                continue

            elif game_state == Scene.LEVELS:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    #Select levels
                    for index, rect in enumerate(level_rects):
                        if rect.collidepoint(event.pos):

                            level_number = index + 1

                            (lily_count, lily_width, board, board_history, arrow_index,
                                is_selected, game_state, lily, indicator, lily_rects,
                                lily_rect, indicator_rect) = start_level(
                                LEVELS[level_number]["board"], level_graphics, WIDTH
                            )

                            crown_index = LEVELS[level_number].get("crown_index", None)
                            if crown_index is not None:
                                crown_history = [crown_index]
                            else:
                                crown_history = []
                            trampoline_indexes = LEVELS[level_number].get("trampoline_indexes", ())
                    #Home button
                    if level_to_home_button_rect.collidepoint(pos):
                        game_state = Scene.HOME

            elif game_state == Scene.WON:
                if event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    if level_number + 1 in LEVELS:
                        level_number += 1

                        (lily_count, lily_width, board, board_history, arrow_index,
                        is_selected, game_state, lily, indicator, lily_rects,
                        lily_rect, indicator_rect) = start_level(
                            LEVELS[level_number]["board"], level_graphics, WIDTH
                        )
                        crown_index = LEVELS[level_number].get("crown_index", None)
                        trampoline_indexes = LEVELS[level_number].get("trampoline_indexes", ())
                        if crown_index is not None:
                            crown_history = [crown_index]
                        else:
                            crown_history = []
                        game_state = Scene.PLAYING
                    else:
                        game_state = Scene.COMPLETE

            elif game_state == Scene.COMPLETE:
                if event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    game_state = Scene.HOME

            elif game_state == Scene.PLAYING:

                #All the mouse controls for the game are handled here.
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(lily_rects):
                        if rect.collidepoint(event.pos):
                            if is_selected == False and board[i] != 0:
                                arrow_index = i
                                is_selected = True
                            elif is_selected == True and arrow_index == i:
                                is_selected = False
                            elif is_selected == True and i in [get_landing_index(arrow_index, board[arrow_index], "left", trampoline_indexes), get_landing_index(arrow_index, board[arrow_index], "right", trampoline_indexes)] and is_valid_landing(i, board, crown_index):
                                board[i] += board[arrow_index]
                                if arrow_index == crown_index:
                                    crown_index = i
                                board[arrow_index] = 0
                                arrow_index = i
                                is_selected = False
                                board_history.append(tuple(board))
                                crown_history.append(crown_index)

                                
                    if undo_button_rect.collidepoint(event.pos) and len(board_history) >1:
                        board_history.pop()
                        board = list(board_history[-1])
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1
                        # if crown_history:
                        #     crown_history.pop()
                        #     crown_index = crown_history[-1]
                    
                    elif menu_button_rect.collidepoint(event.pos):
                        game_state = Scene.HOME

                    elif how_to_play_button_rect.collidepoint(event.pos):
                        game_state = Scene.HOWTOPLAY

                    elif restart_button_rect.collidepoint(event.pos):
                        board = list(LEVELS[level_number]['board'])
                        board_history = [tuple(board)]
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1
                        crown_index = LEVELS[level_number].get("crown_index", None)
                        if crown_index is not None:
                            crown_history = [crown_index]
                        else:
                            crown_history = []
                        

                elif event.type == pg.MOUSEMOTION:
                    for i, rect in enumerate(lily_rects):
                        if rect.collidepoint(event.pos):
                            if is_selected == False:
                                arrow_index = i


                #All the keyboard controls for the game are handled here.
                elif event.type == pg.KEYDOWN:
                    if event.key in [pg.K_a, pg.K_LEFT] and is_selected == False:
                        if arrow_index != 0:
                            arrow_index = arrow_index -1
                            arrow_rect.move_ip(-(WIDTH/lily_count), 0)
                    elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == False:
                        if arrow_index != lily_count -1:
                            arrow_index = arrow_index +1
                    elif event.key in [pg.K_s, pg.K_DOWN] and board[arrow_index]!=0:
                        is_selected = True
                    elif event.key in [pg.K_w, pg.K_UP]:
                        is_selected = False

                    elif event.key in [pg.K_a, pg.K_LEFT] and is_selected == True:
                        landing_index = get_landing_index(arrow_index, board[arrow_index],"left", trampoline_indexes)
                        if is_valid_landing(landing_index, board, crown_index) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            if crown_index == arrow_index:
                                crown_index = landing_index
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(tuple(board))
                            crown_history.append(crown_index)

                    elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == True:
                        landing_index = get_landing_index(arrow_index, board[arrow_index],"right", trampoline_indexes)
                        if is_valid_landing(landing_index, board, crown_index) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            if crown_index == arrow_index:
                                crown_index = landing_index
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(tuple(board))
                            crown_history.append(crown_index)
                            
                    #r is restart
                    elif event.key in [pg.K_r]:
                        board = list(LEVELS[level_number]['board'])
                        board_history = [tuple(board)]
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1
                        crown_index = LEVELS[level_number].get("crown_index", None)
                        if crown_index is not None:
                            crown_history = [crown_index]
                        else:
                            crown_history = []

                    #z is undo
                    elif event.key in [pg.K_z] and len(board_history) >1:
                        board_history.pop()
                        board = list(board_history[-1])
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1
                        if crown_history:
                            crown_history.pop()
                            if crown_history:
                                crown_index = crown_history[-1]

                    #m returns to menu
                    elif event.key in [pg.K_m]:
                        game_state = Scene.HOME
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1
                        
        #Updating part of the loop
        if not running:
            break

        #Drawing part of the loop
        if game_state == Scene.HOME:
            draw_menu(screen)

        elif game_state == Scene.COMPLETE:
            screen.fill("light blue")
            screen.blit(completed_text, (100, 300))

        elif game_state == Scene.HOWTOPLAY:
            tutorial.draw(screen)

        elif game_state == Scene.LEVELS:
            screen.blit(levelscreen, levelscreen_rect)

            # for i in range(0,len(level_rects)):
            #     pg.draw.rect(screen, "red", level_rects[i], 3)

            # pg.draw.rect(screen, "red", level_to_home_button_rect, 3)

            for index, rect in enumerate(level_rects):

                if index + 1 in completed_levels:
                    checkmark_rect.center = rect.center
                    screen.blit(checkmark, checkmark_rect)


                if rect.collidepoint(pos):

                    pg.draw.ellipse(
                        screen,
                        (255, 255, 100),
                        rect,
                        4
                    )

        if game_state == Scene.PLAYING or game_state == Scene.WON:

            #Fill background
            screen.blit(pond, pond_rect)

            #Menu button
            screen.blit(menu_button, menu_button_rect)

            #Undo button
            screen.blit(undo_button, undo_button_rect)

            #how-to-play button
            screen.blit(how_to_play_button, how_to_play_button_rect)

            #Restart button
            screen.blit(restart_button, restart_button_rect)
                

            #Draw the water ripples.
            if is_selected == True:
                indicator_left = get_landing_index(arrow_index, board[arrow_index], "left", trampoline_indexes)
                indicator_right = get_landing_index(arrow_index, board[arrow_index], "right", trampoline_indexes)
                if is_valid_landing(indicator_left, board, crown_index):
                    indicator_rect.center = ((indicator_left + 0.5) * WIDTH//lily_count, int(0.8*HEIGHT))
                    screen.blit(indicator, indicator_rect)
                if is_valid_landing(indicator_right, board, crown_index):
                    indicator_rect.center = ((indicator_right + 0.5)*WIDTH//lily_count, int(0.8*HEIGHT))
                    screen.blit(indicator,indicator_rect)

            # Reuse the rectangles prepared for this board size.
            for lily_rect in lily_rects:
                screen.blit(lily, lily_rect)

            #Draw an ellipse around the lily the mouse is hovering over.
            for rect in lily_rects:
                if rect.collidepoint(pos):
                    pg.draw.ellipse(
                        screen,
                        (255, 255, 100),
                        rect,
                        4
                    )

            #Draw arrow above
            draw_arrow(screen, WIDTH, HEIGHT, arrow, arrow_index, lily_count, is_selected)

            #Draw the frogs
            if lily_count <= 10:
                frog_stack_spacing = int(0.5*frog_width)
            else:
                frog_stack_spacing = int(0.42*frog_width)
            for i in range(0, lily_count):
                if i in trampoline_indexes:
                    trampoline_rect.midbottom = ((i + 0.5)*WIDTH/lily_count, 0.8*HEIGHT)
                    screen.blit(trampoline, trampoline_rect)
                    continue

                for ii in range(board[i]-1, -1, -1):
                    frog_rect.midbottom = ((i + 0.5)*WIDTH/lily_count, 0.8*HEIGHT-(frog_stack_spacing*ii))
                    if i == crown_index and ii == board[i]-1:
                        crown_rect.midbottom = (frog_rect.midtop[0], frog_rect.midtop[1] + 16)
                        screen.blit(crown, crown_rect)
                    screen.blit(frog, frog_rect)

            if player_has_won(board) and game_state == Scene.PLAYING:
                completed_levels.add(level_number)
                game_state = Scene.WON
                
        if game_state == Scene.WON:
            screen.blit(wooden_sign, wooden_sign_rect)
            text_surface1, text_surface2 = win_text[level_number]

            screen.blit(text_surface1, (434, 123))
            screen.blit(text_surface2, (434, 232))
            
    
        pg.display.update()
        # Every screen returns control to the browser once per frame.
        await asyncio.sleep(0)

    pg.quit()


if __name__ == "__main__":
    asyncio.run(main())
