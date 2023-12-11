from board_generator import board1, board2, board3, board4, board5, board6
from forward_checking import forward_checking


class game:
    def __init__(self):
        self.board, self.constraints = board6()
        self.solver = forward_checking(self.board, self.constraints)


def print_board(game_board):
    for row in game_board:
        for col in row:
            if col == 0:
                formatted_text = f"{'':<4}"
            elif col == '#':
                formatted_text = f"{col:<4}"
            else:
                formatted_text = f"{col:<4}"
            print(formatted_text, end='')
        print()
    print("-------------------------------------")

