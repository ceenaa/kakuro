import tkinter as tk
from game import game
from gui import KakuroGUI

if __name__ == "__main__":
    game = game()
    game.solver.solve(-1, -1, game.board, game.solver.constraint_domains, game.solver.constraints_lengths)
    root = tk.Tk()
    app = KakuroGUI(root, game.solver.board, game.constraints)
    root.mainloop()
