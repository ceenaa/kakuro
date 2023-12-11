import tkinter as tk


class KakuroGUI:
    def __init__(self, master, board, constraints):
        self.master = master
        self.master.title("Kakuro Game")
        x = len(board)
        x *= 100
        self.master.geometry(f"{x}x{x}")
        self.master.resizable(False, False)
        self.constraints = constraints
        self.board = board
        self.create_board_widgets()

        for i in range(len(self.board)):
            self.master.grid_rowconfigure(i, weight=1)
            for j in range(len(self.board[i])):
                self.master.grid_columnconfigure(j, weight=1)

    def create_board_widgets(self):
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if col == '#':
                    cell_label = tk.Label(self.master, text="", width=10, height=10, relief="solid", borderwidth=0,
                                          bg="black")

                elif col in self.constraints:
                    cell_label = tk.Canvas(self.master, width=10, height=10, relief="solid", borderwidth=0)
                    d = 0
                    r = 0
                    if 'down' in self.constraints[col]:
                        d = self.constraints[col]['down']
                    if 'right' in self.constraints[col]:
                        r = self.constraints[col]['right']
                    size = 100
                    x = i * size
                    y = j * size
                    draw_square(cell_label, 0, 0, size, d, r)

                else:
                    if col == 0:
                        text = ""
                    else:
                        text = str(col)
                    cell_label = tk.Label(self.master, text=text, width=10, height=10, relief="solid", border=0.5)

                cell_label.grid(row=i, column=j, sticky="nsew")


def draw_square(canvas, x, y, size, down, right):
    canvas.create_rectangle(x, y, x + size, y + size, outline="black")

    center_x1 = x + (size / 4)
    center_y1 = y + (3 * size / 4)

    center_x2 = x + (3 * size / 4)
    center_y2 = y + (size / 4)

    if down == 0:
        canvas.create_polygon(x, y, x + size, y + size, x, y + size, fill="black", outline="black")
    else:
        canvas.create_polygon(x, y, x + size, y + size, x, y + size, fill="white", outline="black")
        canvas.create_text(center_x1, center_y1, text=f"{down}", fill="black")

    if right == 0:
        canvas.create_polygon(x, y, x + size, y + size, x + size, y, fill="black", outline="black")

    else:
        canvas.create_polygon(x, y, x + size, y + size, x + size, y, fill="white", outline="black")
        canvas.create_text(center_x2, center_y2, text=f"{right}", fill="black")
