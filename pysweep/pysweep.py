from Tkinter import *
from math import floor
from random import randint

from mineboard import Mineboard


if __name__ == "__main__":
    root = Tk()
    root.title('Pysweep')
    minefield = Mineboard(rows=15,
                          cols=20,
                          tilesize=20,
                          margin=20)
    while 1:
        try:
            root.update()
        except Exception as e:
            exit()
