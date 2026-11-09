from enum import Enum

#Specify the scenes that the player can be in
class Scene(Enum):
        HOME = 1
        HOWTOPLAY = 2
        LEVELS = 3
        CREDITS = 4
        PLAYING = 5
        WON = 6
        COMPLETE = 7

game_state = Scene.HOME