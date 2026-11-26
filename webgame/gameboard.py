import math

class GameBoard:
    def __init__(self, board: list[int], crown_index: int = None, trampoline_indexes: tuple(int) = None, function = None):
        self.board = board
        self.crown_index = crown_index
        self.trampoline_indexes = trampoline_indexes
        self.history = [{"board": board, "crown_index": crown_index}]
        self.is_selected = False
        self.arrow_index = math.ceil(len(self.board)/2) -1
        if function is None:
            self.function = lambda x: 2 * x - 1

    def check_win(self) -> bool:
        """Returns True if the player has won the game, False otherwise."""
        return max(self.board) == sum(self.board)

    def get_jump_distance(self, frog_count:int) -> int:
        """Returns the distance a frog can jump based on the number of frogs on the lily pad."""
        if frog_count == 0:
            return 0
        else:
            return self.function(frog_count)

    def get_landing_index(self, arrow_index:int, frog_count:int, direction:str) -> int:
        """Returns the index of the lily pad the frog will land on"""
        distance = self.get_jump_distance(frog_count)

        if direction == "left":
            if arrow_index - distance in self.trampoline_indexes:
                 return arrow_index - (2 * distance)
            else:
                return arrow_index -distance
        elif direction == "right":
            if arrow_index + distance in self.trampoline_indexes:
                 return arrow_index + (2 * distance)
            else:
                return arrow_index + distance

    def is_valid_landing(self, landing_index:int, board:list = [], crown_index:int = None) -> bool:
        """Returns True if the landing index is valid, False otherwise."""
        if landing_index < 0 or landing_index >= len(self.board):
            return False #Cannot land out of bounds
        elif self.board[landing_index] == 0:
            return False #Cannot land on empty lily
        elif landing_index == crown_index: 
                    return False #Cannot land on crown
        else:
            return True
        

    def undo(self):
        """undo the last move, by removing it from the history"""
        if len(self.history) <= 1:
            return
        self.history.pop()
        board = self.history[-1]['board']
        crown_index = self.history[-1]['corwn_index']
        trampoline_indexes = self.history[-1]['trampoline_indexes']
        self.is_selected = False
        self.arrow_index = math.ceil(len(self.board)/2) -1

    def reset(self):
        """resets the game to the beginning of the level"""
        board = self.history[0]['board']
        crown_index = self.history[0]['crown_index']
        self.history = [self.history[0]]
        self.is_selected = False
        arrow_index = math.ceil(len(self.board)/2) -1
        
    

    
        