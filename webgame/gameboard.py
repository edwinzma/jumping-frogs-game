class GameBoard:
    def __init__(self, board, crown_index = None, function = None):
        self.board = board
        if crown_index is not None:
            self.crown_index = crown_index

        self.history = [{"board": board, "crown_index": crown_index}]
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
            return arrow_index -distance
        elif direction == "right":
            return arrow_index + distance

    def is_valid_landing(landing_index:int, board:list = [], crown_index:int = None) -> bool:
        """Returns True if the landing index is valid, False otherwise."""
        if landing_index < 0 or landing_index >= len(self.board):
            return False #Cannot land out of bounds
        elif self.board[landing_index] == 0:
            return False #Cannot land on empty lily
        elif landing_index == crown_index: 
                    return False #Cannot land on crown
        else:
            return True
    

    
        