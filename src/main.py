from Tkinter import *
from math import floor
from random import randint

from mineboard import Mineboard


if __name__ == "__main__":
    root = Tk()
    tilesize = 20
    margin = 20
    rows = 20
    cols = 30
    board = Canvas(root, width=tilesize*cols+margin*2, height=tilesize*rows+margin*2)
    minefield = Mineboard(board, rows = rows, cols = cols, tilesize = tilesize, margin_width = margin, margin_height = margin)

    minefield.populateBoard()

    minefield.bindBoardEvents()

    board.pack()
    root.mainloop()
