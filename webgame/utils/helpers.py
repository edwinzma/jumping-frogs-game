#PART 1: Define functions
import pygame as pg

#from button import Button


def player_has_won(board_state:list) -> bool:
    """Returns True if the player has won the game, False otherwise. The player wins if all frogs are on the same lily pad."""
    return max(board_state) == sum(board_state)


def get_jump_distance(frog_count:int) -> int:
    """Returns the distance a frog can jump based on the number of frogs on the lily pad. The distance is 2*frog_count - 1. If there are no frogs, the distance is 0."""
    if frog_count == 0:
        return 0
    else:
        return 2*frog_count -1


def get_landing_index(arrow_index:int, frog_count:int, direction:str) -> int:
    """Returns the index of the lily pad the frog will land on"""
    distance = get_jump_distance(frog_count)

    if direction == "left":
        return arrow_index -distance
    elif direction == "right":
        return arrow_index + distance


def is_valid_landing(landing_index:int, board:list = [], crown_index:int = None) -> bool:
    """Returns True if the landing index is valid, False otherwise. A landing index is valid if it is within the bounds of the board and there is at least one frog on the lily pad."""
    if landing_index == crown_index:
        return False
    if landing_index >=0 and landing_index <len(board) and board[landing_index] > 0:
        return True
    else:
        return False


def draw_lilies(screen:tuple, width:int, height:int, image, lily_count:int) -> int:
    """Draws the lily pads on the screen. The lily pads are evenly spaced across the width of the screen."""
    for i in range(0,lily_count):
        lily_rect = image.get_rect()
        lily_rect.center = ((i+0.5)*width//lily_count, int(0.8*height))

        dummy = None
        if Button(image, lily_rect).draw(screen):
            dummy = i
    return dummy


def draw_arrow(screen, width, height, image, arrow_index, lilypad_count, is_selected):
    """Draws the arrow on the screen."""
    arrow_rect = image.get_rect()
    arrow_rect.center = ((arrow_index+0.5)*width/lilypad_count, 0.3*height+is_selected*0.1*height)
    screen.blit(image, arrow_rect)


def set_lily_width(lilypad_count:int, width:int) -> int:
    """Returns the width of the lily pad based on the number of lily pads and the width of the screen. 
    The width is set to be the minimum of the width of the screen divided by the number of lily pads minus 10 and 200. 
    This ensures that the lily pads are not too small or too large."""
    return int(min(width/lilypad_count - 10, 200))


def set_lily_height() -> int:
    """Returns the height of the lilypad. The height is set to be 70 pixels for now."""
    return 70


def set_frog_width(lilypad_count:int = 4, WIDTH  = 1280) -> int:
    """Returns the width of the frog. The width is set to be 102 pixels for now."""
    return int(min(102, WIDTH/lilypad_count - 10))


def set_frog_height(frog_width:int = 102) -> int:
    """Returns the height of the frog. The height is set to be 70 pixels for now."""
    return int(frog_width * 70 / 102)


def get_level_rectangles() -> list:
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


def start_level(starting_board: tuple, level_graphics: dict, width: int) -> tuple:
    """Return reset gameplay state and the prepared graphics for a level."""
    lily_count = len(starting_board)
    board_history = [starting_board]
    board = list(starting_board)
    arrow_index = lily_count // 2
    is_selected = False
    game_state = "playing"
    lily_width = set_lily_width(lily_count, width)
    # Reuse prepared graphics; no resizing here.
    lily, indicator, lily_rects = level_graphics[lily_count]
    lily_rect = lily.get_rect()
    indicator_rect = indicator.get_rect()

    return (
        lily_count, lily_width, board, board_history, arrow_index,
        is_selected, game_state, lily, indicator, lily_rects,
        lily_rect, indicator_rect,
    )
