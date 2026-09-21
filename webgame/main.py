import os
import asyncio
import pygame as pg
import math

#First define all functions

#A player has won when all frogs are on one lilypad. This means that the max number = sum. Could add another win condition later
def player_has_won(board_state:list) -> bool:
    return max(board_state) == sum(board_state)

#Jumping distance is determined at n frogs leap 2n-1. This can be easily changed by changing this function only
def get_jump_distance(frog_count:int) -> int:
    if frog_count == 0:
        return 0
    else:
        return 2*frog_count -1

#Check landing index
def get_landing_index(arrow_index:int, frog_count:int, direction:str) -> int:
    distance = get_jump_distance(frog_count)

    if direction == "left":
        return arrow_index -distance
    elif direction == "right":
        return arrow_index + distance

def is_valid_landing(landing_index:int, current_state:list) -> bool:
    if landing_index >=0 and landing_index <len(current_state) and current_state[landing_index] > 0:
        return True
    else:
        return False

def draw_lilypads(screen:tuple, width:int, height:int, image, lilypad_count:int):
    for i in range(0,lilypad_count):
        lilypad_rect = image.get_rect()
        lilypad_rect.center = ((i+0.5)*width//lilypad_count, int(0.8*height))
        screen.blit(image, lilypad_rect)

def draw_arrow(screen, width, height, image, arrow_index, lilypad_count, is_selected):
    arrow_rect = image.get_rect()
    arrow_rect.center = ((arrow_index+0.5)*width/lilypad_count, 0.3*height+is_selected*0.1*height)
    screen.blit(image, arrow_rect)

def set_lilypad_width(lilypad_count:int, width:int) -> int:
    return int(min(width/lilypad_count - 10, 200))

def set_lilypad_height() -> int:
    return 70

def set_frog_width() -> int:
    return 102



#Draw rectangles needed for levels-screen. Manually calibrated for a (1280,720) screen.
def get_level_rects() -> list:
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

class HowToPlay:
    """Three tutorial pages, drawn with text and the game's existing sprites."""

    def __init__(self, pond, frog, lilypad):
        self.pond = pond
        # Scale once, rather than resizing images on every frame.
        self.frog = pg.transform.smoothscale(frog, (76, 76))
        self.lilypad = pg.transform.smoothscale(lilypad, (132, 46))
        self.title_font = pg.font.Font(None, 56)
        self.body_font = pg.font.Font(None, 34)
        self.small_font = pg.font.Font(None, 27)
        self.menu_rect = pg.Rect(64, 624, 200, 54)
        self.back_rect = pg.Rect(824, 624, 170, 54)
        self.next_rect = pg.Rect(1010, 624, 206, 54)
        self.reset()

    def reset(self):
        self.page = 0
        self.example_step = 0

    def advance(self):
        if self.page < 2:
            self.page += 1
        elif self.example_step < 3:
            self.example_step += 1
        else:
            return "home"
        return None

    def back(self):
        if self.page == 2 and self.example_step > 0:
            self.example_step -= 1
        elif self.page > 0:
            self.page -= 1

    def handle_event(self, event):
        # Return a new game state only when leaving the tutorial.
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_ESCAPE, pg.K_m):
                return "home"
            if event.key == pg.K_LEFT:
                self.back()
            elif event.key in (pg.K_RIGHT, pg.K_SPACE, pg.K_RETURN):
                return self.advance()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_rect.collidepoint(event.pos):
                return "home"
            if self.back_rect.collidepoint(event.pos):
                self.back()
            elif self.next_rect.collidepoint(event.pos):
                return self.advance()
        return None

    def text(self, screen, message, center, small=False, title=False,
             color=(31, 65, 43)):
        font = self.title_font if title else self.small_font if small else self.body_font
        surface = font.render(message, True, color)
        screen.blit(surface, surface.get_rect(center=center))

    def button(self, screen, rect, label, enabled=True):
        hovered = rect.collidepoint(pg.mouse.get_pos())
        color = (61, 126, 70) if hovered else (37, 91, 53)
        if not enabled:
            color = (139, 150, 133)
        pg.draw.rect(screen, color, rect, border_radius=14)
        self.text(screen, label, rect.center, color=(255, 250, 226))

    def board(self, screen, counts, centers, y, selected=None, targets=()):
        """Draw a small example without changing the real game's board."""
        for index, (count, x) in enumerate(zip(counts, centers)):
            if index in targets:
                pg.draw.ellipse(screen, (39, 164, 219), (x-77, y-29, 154, 58), 4)
                pg.draw.ellipse(screen, (128, 216, 242), (x-85, y-35, 170, 70), 2)
            screen.blit(self.lilypad, self.lilypad.get_rect(center=(x, y)))
            for height in range(count-1, -1, -1):
                rect = self.frog.get_rect(midbottom=(x, y-5-height*30))
                screen.blit(self.frog, rect)
            self.text(screen, str(count), (x, y+43), small=True)
            if index == selected:
                tip_y = y-92-max(0, count-1)*30
                pg.draw.line(screen, (35, 64, 42), (x, tip_y-26), (x, tip_y-7), 5)
                pg.draw.polygon(screen, (35, 64, 42),
                                [(x-10, tip_y-12), (x+10, tip_y-12), (x, tip_y)])

    def draw(self, screen):
        screen.blit(self.pond, (0, 0))
        pg.draw.rect(screen, (255, 249, 222), (40, 28, 1200, 578), border_radius=24)
        pg.draw.rect(screen, (77, 119, 59), (40, 28, 1200, 578), 3, border_radius=24)
        titles = ["Your goal", "How far can frogs jump?", "A four-frog example"]
        self.text(screen, titles[self.page], (640, 78), title=True)
        self.text(screen, f"HOW TO PLAY  |  {self.page+1} / 3", (640, 120), small=True)

        if self.page == 0:
            self.text(screen, "Get all frogs onto one lily pad.", (640, 172))
            self.board(screen, [1, 1, 1, 1], [145, 285, 425, 565], 372)
            self.board(screen, [4, 0, 0, 0], [735, 875, 1015, 1155], 372)
            pg.draw.line(screen, (37, 91, 53), (627, 329), (662, 329), 5)
            pg.draw.polygon(screen, (37, 91, 53), [(652, 319), (669, 329), (652, 339)])
            self.text(screen, "Start: frogs on separate pads", (355, 448))
            self.text(screen, "Goal: all frogs together", (945, 448))
            self.text(screen, "Move the selector with Left / Right. Press Down to select frogs.", (640, 514))
            self.text(screen, "Then press Left / Right to jump. Press Up to deselect.", (640, 552))

        elif self.page == 1:
            self.text(screen, "All frogs on the selected pad jump together.", (640, 170))
            self.board(screen, [1, 2, 3], [275, 640, 1005], 350)
            for x, label in zip([275, 640, 1005],
                                ["1 frog: 1 space", "2 frogs: 3 spaces", "3 frogs: 5 spaces"]):
                self.text(screen, label, (x, 422))
            self.text(screen, "The rule: n frogs jump exactly 2n - 1 spaces, left or right.", (640, 466))
            pg.draw.rect(screen, (255, 222, 135), (95, 499, 1090, 82), border_radius=14)
            self.text(screen, "Only land on a pad that already contains a frog.", (640, 524))
            self.text(screen, "Count every space, including empty pads you jump over.", (640, 555), small=True)

        else:
            states = [[1, 1, 1, 1], [1, 1, 0, 2], [3, 1, 0, 0], [4, 0, 0, 0]]
            captions = ["Select the third frog. Jump 1 space to the right.",
                        "Now select the pair on the right. Jump 3 spaces to the left.",
                        "Select the last single frog. Jump 1 space to the left.",
                        "All four frogs are together. You win!"]
            selected = [2, 3, 1, None][self.example_step]
            targets = [(1, 3), (0,), (0,), ()][self.example_step]
            self.text(screen, captions[self.example_step], (640, 178))
            self.board(screen, states[self.example_step], [295, 525, 755, 985],
                       402, selected=selected, targets=targets)
            self.text(screen, "Blue ripples show the possible landing pads.", (640, 481), small=True)
            self.text(screen, "Click Next move to see what happens." if self.example_step < 3
                      else "Ready to try it in the game?", (640, 516))
            self.text(screen, "In the game: Z = undo    R = restart    M = main menu", (640, 560), small=True)

        self.button(screen, self.menu_rect, "Main menu")
        self.button(screen, self.back_rect, "Back", self.page > 0)
        label = "Next page" if self.page < 2 else "Next move" if self.example_step < 3 else "Done"
        self.button(screen, self.next_rect, label)
        self.text(screen, "Left / Right: browse   |   Esc: menu", (543, 651), small=True,
                  color=(255, 255, 255))


# async is needed for webapp
async def main():

    SIZE: tuple             = (1280,720)
    WIDTH:int               = SIZE[0]
    HEIGHT:int              = SIZE[1]
    game_state: str         = "home" #game states are "home", "htp", "playing", "won"
    lilypad_count: int      = 4 # Amount of lilypad at the starting level
    lilypad_width: int      = set_lilypad_width(lilypad_count, WIDTH)
    lilypad_height: int     = set_lilypad_height()
    frog_width: int         = set_frog_width()
    arrow_index: int        = 2 # position of the selector
    board: [int]            = [1]*lilypad_count #Starting position of the frogs
    arrow_rect: pg.Rect     = pg.Rect(0, 0, 100, 100) #dummy variable, later used for selector
    is_selected: bool       = False #Has the player selected anything. Start of as False
    board_history: [list]   = [board.copy()] #This memories all the previous states of the game at that level to enable undoing with z
    indicator_scalar: float = 1.4 #F stands for factor, which is the factor by which the indicator width and height are multiplied by the width and height of the lilypad
    clicked: bool           = False #Is the mouse clicked. Used to prevent multiple clicks from being registered when the mouse is held down.

    #initialize Pygame
    pg.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Jumping Frogs")
    clock = pg.time.Clock()
    my_font = pg.font.SysFont("Comic Sans MS", 30)
    
    #apply changes
    pg.display.update()


    def start_level(level_number:int) ->None:

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


        lilypad_count = level_number + 4

        board = [1] * lilypad_count
        board_history = [board.copy()]

        arrow_index = lilypad_count // 2
        is_selected = False
        game_state = "playing"


        lilypad_width = int(min(WIDTH/lilypad_count - 10, 200))
        lilypad_rect = pg.Rect(0,0,lilypad_width, lilypad_height)
        lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
        indicator = pg.transform.scale(indicator_original, (int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar)))
        indicator_rect = pg.Rect(0,0,int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar))

    level_rects = get_level_rects()
    level_to_home_button_rect = pg.Rect(1045, 605, 206, 74)

    #load images
    screen_rect = pg.Rect(0,0,WIDTH, HEIGHT)

    pond_original = pg.image.load("pond.png").convert_alpha()
    pond = pg.transform.scale(pond_original, (WIDTH, HEIGHT))
    pond_rect = pond.get_rect()


    homescreen_original = pg.image.load("Homescreen.png").convert_alpha()
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

    #Main loop
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

            if game_state == "levels": #Player is at the levels-screen
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        for index, rect in enumerate(level_rects):

                            if rect.collidepoint(event.pos):

                                level_number = index + 1

                                print("Selected level:", level_number)
                                start_level(level_number)
                                
                        if level_to_home_button_rect.collidepoint(pos):
                            game_state = "home"


            if event.type == pg.KEYDOWN:

                if game_state == "won":
                    game_state = "playing"

                elif game_state == "playing":
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
                            board_history.append(board.copy())

                    elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == True:

                        landing_index = get_landing_index(arrow_index, board[arrow_index],"right")
                        if is_valid_landing(landing_index, board) == True:
                            board[landing_index] = board[landing_index] +board[arrow_index]
                            board[arrow_index] = 0
                            arrow_index = landing_index
                            is_selected = False
                            board_history.append(board.copy())
                                
                    #r is restart
                    elif event.key in [pg.K_r]:
                        board = [1]*lilypad_count
                        board_history = [board.copy()]
                        is_selected = False
                        arrow_index = math.ceil(lilypad_count/2) -1

                    #z is undo
                    elif event.key in [pg.K_z] and len(board_history) >1:
                        board_history.pop()
                        board = board_history[-1].copy()
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

            #Draw lilypads
            if is_selected == True:
                indicator_left = get_landing_index(arrow_index, board[arrow_index], "left")
                indicator_right = get_landing_index(arrow_index, board[arrow_index], "right")
                if is_valid_landing(indicator_left, board):
                    indicator_rect.center = ((indicator_left + 0.5) * WIDTH//lilypad_count, int(0.8*HEIGHT))
                    screen.blit(indicator, indicator_rect)
                if is_valid_landing(indicator_right, board):
                    indicator_rect.center = ((indicator_right + 0.5)*WIDTH//lilypad_count, int(0.8*HEIGHT))
                    screen.blit(indicator,indicator_rect)

            draw_lilypads(screen, WIDTH, HEIGHT, lilypad, lilypad_count)

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
                lilypad_count += 1
                board = [1]*lilypad_count
                board_history = [board.copy()]
                lilypad_width = int(min(WIDTH/lilypad_count - 10, 200))
                lilypad_rect = pg.Rect(0,0,lilypad_width, lilypad_height)
                lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
                indicator = pg.transform.scale(indicator_original, (int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar)))
                indicator_rect = pg.Rect(0,0,int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar))
                game_state = "won"
                
        if game_state == "won":
            screen.blit(wooden_sign, wooden_sign_rect)

            # sign_rect = pg.Rect(400, 200, 480, 200)
            # pg.draw.rect(screen, "brown", sign_rect)
            text_surface1 = my_font.render("Congrats! You win level "+ str(lilypad_count-4) + "!", False, (0, 0, 0))
            text_surface2 = my_font.render("Press any key to continue to level  "+ str(lilypad_count-4) + ".", False, (0, 0, 0))
            
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