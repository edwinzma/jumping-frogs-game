"""
Created by Edwin Ma. Check out my GitHub at: https://github.com/edwinzma
"""
import sys
import math
import config

import asyncio
import pygame as pg
from pygame import mixer

from config import SIZE, WIDTH, HEIGHT, lily_count, lily_width, lily_height, frog_width, arrow_rect, indicator_scalar, is_music_on, LEVELS, MUSIC
from htp import HowToPlay
from utils.helpers import draw_speaker, player_has_won, get_landing_index, is_valid_landing, draw_arrow, set_lily_width, set_lily_height, get_level_rectangles


# async is needed for webapp
async def main():
    # Initialize state here because assignments below make these variables local.
    level_number = config.level_number
    game_state = config.game_state
    board = list(config.board)
    board_history = list(config.board_history)
    arrow_index = config.arrow_index
    is_selected = config.is_selected
    clicked = config.clicked

    in_browser = sys.platform == "emscripten"
    if MUSIC:
        if in_browser:
            print("initializing pygame for browser...")
            #pg.init() would also open SDL audio, even though music uses the browser.
            pg.display.init()
            pg.font.init()
        else:
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
            pg.init()
    else:
        pg.init()

    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Jumping Frogs")
    clock = pg.time.Clock()
    my_font = pg.font.SysFont("Comic Sans MS", 30)

    
    #apply changes
    pg.display.update()

    def toggle_music():

        global is_music_on
        nonlocal main_channel

        is_music_on = not is_music_on
        if is_music_on:
            mixer.music.unpause()
            main_channel.set_volume(0.1)
        else:
            mixer.music.pause()
            main_channel.set_volume(0)

    def start_level(level_number:int, starting_board:tuple) ->None:

        global lily_count
        global lily_width
        nonlocal lilypad_rect
        nonlocal lilypad
        nonlocal indicator
        nonlocal indicator_rect
        nonlocal board
        nonlocal board_history
        nonlocal arrow_index
        nonlocal is_selected
        nonlocal game_state
        nonlocal lilypad_rects


        lily_count = len(starting_board)

        board_history = [starting_board]
        board = list(starting_board)
        

        arrow_index = lily_count // 2
        is_selected = False
        game_state = "playing"

        lily_width = set_lily_width(lily_count, WIDTH)
        lilypad_height = set_lily_height()
        lilypad_rect = pg.Rect(0,0,lily_width, lilypad_height)
        # Reuse graphics prepared before music playback; no resizing here.
        lilypad, indicator, lilypad_rects = level_graphics[lily_count]
        lilypad_rect = lilypad.get_rect()
        indicator_rect = indicator.get_rect()

    level_rects = get_level_rectangles()
    level_to_home_button_rect = pg.Rect(1045, 605, 206, 74)

    #PART 2: load images
    screen_rect = pg.Rect(0,0,WIDTH, HEIGHT)

    pond_original = pg.image.load("assets/images/pond.png").convert_alpha()
    pond = pg.transform.scale(pond_original, (WIDTH, HEIGHT))
    pond_rect = pond.get_rect()

    # homescreen_original = pg.image.load("Homescreen.png").convert_alpha()
    # homescreen = pg.transform.scale(homescreen_original, (WIDTH, HEIGHT))
    # homescreen_rect = homescreen.get_rect()


    homescreen_original = pg.image.load("assets/images/Homescreen.png").convert_alpha()
    homescreen = pg.transform.scale(homescreen_original, (WIDTH, HEIGHT))
    homescreen_rect = homescreen.get_rect()



    levelscreen_original = pg.image.load("assets/images/level_screen.png").convert_alpha()
    levelscreen = pg.transform.scale(levelscreen_original, (WIDTH, HEIGHT))
    levelscreen_rect = levelscreen.get_rect()

    title_original = pg.image.load("assets/images/name_of_game.png").convert_alpha()
    title = pg.transform.scale(title_original, (250,200))
    title_rect = title.get_rect()

    frog_original = pg.image.load("assets/images/frog.png").convert_alpha()
    frog = pg.transform.scale(frog_original, (frog_width,frog_width))
    frog_rect = frog.get_rect()

    Lilypad_original = pg.image.load("assets/images/lilypad.png").convert_alpha()
    lilypad = pg.transform.scale(Lilypad_original, (lily_width, lily_height))
    lilypad_rect = lilypad.get_rect()

    indicator_original = pg.image.load("assets/images/landing_indicator2.png").convert_alpha()
    visible_rect = indicator_original.get_bounding_rect()
    indicator_original = indicator_original.subsurface(visible_rect).copy()
    indicator = pg.transform.scale(indicator_original, (int(lily_width *indicator_scalar), int(lily_height*indicator_scalar)))
    indicator_rect = indicator.get_rect()

    arrow_original = pg.image.load("assets/images/arrow.png").convert_alpha()
    arrow = pg.transform.scale(arrow_original, (100, 100))
    arrow_loc = arrow.get_rect()
    arrow_loc.center = 0.5*WIDTH/lily_count, HEIGHT*0.2

    wooden_sign_original = pg.image.load("assets/images/wooden_sign.png").convert_alpha()
    wooden_sign = pg.transform.scale(wooden_sign_original, (1000, 600))
    wooden_sign_rect = wooden_sign.get_rect()
    wooden_sign_rect.midtop = (640, -100)

    menu_button_original = pg.image.load("assets/images/menu_button.png").convert_alpha()
    menu_button = pg.transform.scale(menu_button_original, (250,126))
    menu_button_rect = menu_button.get_rect()
    menu_button_rect.topright = (1270,0)

    #DRAW rectangles over play-button, How-to-Play button on the home screen.
    play_button_rect = pg.Rect(472, 332, 343, 90)
    htp_button_rect = pg.Rect(472, 447, 343, 77)
    levels_button_rect = pg.Rect(472,554, 343, 77)

    speaker_on_original = pg.image.load("assets/images/speaker.png").convert_alpha()
    speaker_on = pg.transform.scale(speaker_on_original, (50,50))
    speaker_off_original = pg.image.load("assets/images/speaker-off.png").convert_alpha()
    speaker_off = pg.transform.scale(speaker_off_original, (50,50))
    speaker_rect = speaker_on.get_rect()
    speaker_rect.topleft = (50,50)




    # Tutorial owns its page number and example; it never changes the real board.
    tutorial = HowToPlay(pond, frog_original, Lilypad_original)

    # Prepare every board size before audio starts.
    level_graphics = {}
    for count in sorted({lily_count} | {len(board) for board in LEVELS.values()}):
        pad_width = set_lily_width(count, WIDTH)
        pad = pg.transform.scale(Lilypad_original, (pad_width, lily_height))
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
    lilypad, indicator, lilypad_rects = level_graphics[lily_count]
    lilypad_rect = lilypad.get_rect()
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

    
    if MUSIC:
        # Start music only after image loading, resizing and tutorial setup finish.
        if not in_browser:
            mixer.music.load("assets/music/02_Lily_Pad_Hop.ogg")
            mixer.music.set_volume(0.1)
        screen.blit(homescreen, homescreen_rect)
        pg.display.update()
        await asyncio.sleep(0)
        if in_browser:
            from browser_support import start_music, stop_music
            start_music("assets/music/02_Lily_Pad_Hop.ogg")
            if not is_music_on:
                stop_music()
        elif is_music_on:
            mixer.music.play(-1, fade_ms=1000)

        main_channel = mixer.Channel(0)
        jump_sound = mixer.Sound("assets/sounds/jump_01.ogg")
        jump_sound.set_volume(0.1)

    #PART 3: Main loop
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

            if game_state == "home":
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and (clicked == False) and speaker_rect.collidepoint(event.pos):
                        toggle_music()

            if game_state == "htp":
                next_state = tutorial.handle_event(event)
                if next_state is not None:
                    game_state = next_state
                # Do not let tutorial navigation also trigger gameplay controls.
                continue

            elif game_state == "levels": #Player is at the levels-screen
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Toggle music
                        if speaker_rect.collidepoint(event.pos) and clicked == False:
                            if MUSIC:
                                toggle_music()

                        #Select levels
                        for index, rect in enumerate(level_rects):

                            if rect.collidepoint(event.pos):

                                level_number = index + 1

                                start_level(level_number, LEVELS[level_number])
                        #Home button
                        if level_to_home_button_rect.collidepoint(pos):
                            game_state = "home"

            elif game_state == "won":
                if event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    if level_number + 1 in LEVELS:
                        level_number += 1
                        start_level(level_number, LEVELS[level_number])
                        game_state = "playing"
                    else:
                        game_state = "complete"

            elif game_state == "complete":
                if event.type == pg.KEYDOWN or (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
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
                                    if MUSIC:
                                        main_channel.play(jump_sound)

                        if speaker_rect.collidepoint(event.pos) and clicked == False:
                            toggle_music()



                #All the keyboard controls for the game are handled here.
                if event.type == pg.KEYDOWN:
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
                        landing_index = get_landing_index(arrow_index, board[arrow_index],"left")
                        if is_valid_landing(landing_index, board) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(tuple(board))
                            if MUSIC:
                                main_channel.play(jump_sound)

                    elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == True:
                        landing_index = get_landing_index(arrow_index, board[arrow_index],"right")
                        if is_valid_landing(landing_index, board) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(tuple(board))
                            if MUSIC:
                                main_channel.play(jump_sound)
                            
                    #r is restart
                    elif event.key in [pg.K_r]:
                        board = [1]*lily_count
                        board_history = [tuple(board)]
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1

                    #z is undo
                    elif event.key in [pg.K_z] and len(board_history) >1:
                        board_history.pop()
                        board = list(board_history[-1])
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1

                    #m returns to menu
                    elif event.key in [pg.K_m]:
                        game_state = "home"
                        is_selected = False
                        arrow_index = math.ceil(lily_count/2) -1
                        
        #Updating part of the loop
        if not running:
            break

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
            draw_speaker(screen, speaker_on, speaker_off, speaker_rect, is_music_on)

        elif game_state == "complete":
            screen.fill("light blue")
            screen.blit(completed_text, (100, 300))

        elif game_state == "htp":
            tutorial.draw(screen)

        elif game_state == "levels":
            screen.blit(levelscreen, levelscreen_rect)
            draw_speaker(screen, speaker_on, speaker_off, speaker_rect, is_music_on)

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
            draw_speaker(screen, speaker_on, speaker_off, speaker_rect, is_music_on)

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
                    indicator_rect.center = ((indicator_left + 0.5) * WIDTH//lily_count, int(0.8*HEIGHT))
                    screen.blit(indicator, indicator_rect)
                if is_valid_landing(indicator_right, board):
                    indicator_rect.center = ((indicator_right + 0.5)*WIDTH//lily_count, int(0.8*HEIGHT))
                    screen.blit(indicator,indicator_rect)

            # Reuse the rectangles prepared for this board size.
            for lilypad_rect in lilypad_rects:
                screen.blit(lilypad, lilypad_rect)

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
            draw_arrow(screen, WIDTH, HEIGHT, arrow, arrow_index, lily_count, is_selected)

            #Draw the frogs
            if lily_count <= 10:
                frog_stack_spacing = int(0.5*frog_width)
            else:
                frog_stack_spacing = int(0.42*frog_width)
            for i in range(0, lily_count):
                for ii in range(board[i]-1, -1, -1):
                    frog_rect.midbottom = ((i + 0.5)*WIDTH/lily_count, 0.8*HEIGHT-(frog_stack_spacing*ii))
                    screen.blit(frog, frog_rect)

            if player_has_won(board) and game_state == "playing":
                game_state = "won"
                
        if game_state == "won":
            screen.blit(wooden_sign, wooden_sign_rect)
            text_surface1, text_surface2 = win_text[level_number]

            screen.blit(text_surface1, (434, 123))
            screen.blit(text_surface2, (434, 232))


        if pg.mouse.get_pressed()[0] == 1 and clicked == False:
            clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            clicked = False      

            
    
        pg.display.update()
        # Every screen returns control to the browser once per frame.
        await asyncio.sleep(0)

    # Graceful quit when the game receives QUIT. Closing a browser tab can
    # terminate execution before this runs, so tab-close clicks aren't guaranteed.
    if in_browser:
        stop_music()
    elif mixer.get_init():
        volume = mixer.music.get_volume()
        fade_started = pg.time.get_ticks()
        while mixer.music.get_busy():
            progress = min((pg.time.get_ticks() - fade_started) / 200, 1.0)
            mixer.music.set_volume(volume * (1.0 - progress))
            if progress >= 1.0:
                break
            pg.event.pump()
            await asyncio.sleep(0.01)
        mixer.music.stop()
        mixer.stop()
    pg.quit()


if __name__ == "__main__":
    asyncio.run(main())
