from Tkinter import *
from math import floor
from random import randint

from menu import Menu
from mineboard import Mineboard


if __name__ == "__main__":
    root = Tk()
    root.title('Pysweep')

    minefield = Mineboard(rows=15, cols=20, tilesize=20, margin_width=20, margin_height=20)
    minefield.setup()

    menu = Menu()

    root.mainloop()
