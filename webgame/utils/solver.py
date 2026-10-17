from helpers import *


def solvable(board: list[int], crown_index: int = None) -> bool:
    stack = [(board, crown_index)]
    visited = set()

    while stack:
        current_board, crown_index = stack.pop()
        if (tuple(current_board), crown_index) in visited:
            continue
        else:
            visited.add((tuple(current_board), crown_index))
        if player_has_won(current_board):
            return True

        for i in range(len(current_board)):
            if current_board[i] > 0:
                for direction in ["left", "right"]:
                    landing_index = get_landing_index(i, current_board[i], direction)
                    if is_valid_landing(landing_index, current_board, crown_index):
                        if i == crown_index:
                            crown_index = landing_index
                        new_board = current_board.copy()
                        new_board[landing_index] += new_board[i]
                        new_board[i] = 0
                        stack.append((new_board, crown_index))
    else:
        return False
    


if __name__ == "__main__":
    print(solvable([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 0))


        

    
    

