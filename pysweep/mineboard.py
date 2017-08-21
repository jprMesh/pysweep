from Tkinter import *
from math import floor
from random import randint
from time import time as currenttime

class Mineboard(Frame):
    '''
    Class representing the mineboard where the game is played. Contains board,
    mines, all GUI, and all logic for handling input. Extends Tkinter's
    Frame class.
    '''
    def __init__(self,
                 mine_density = 0.15,
                 rows = 20,
                 cols = 30,
                 tilesize = 20,
                 margin = 20):

        Frame.__init__(self)
        self.grid(row=0, column=0)
        self.focus_set()
        self.margin_top = 50
        self.board = Canvas(self,
                            width = 2*margin + cols*tilesize,
                            height = (margin + rows*tilesize + self.margin_top))
        self.board.pack()

        self.rows = rows
        self.cols = cols
        self.tilesize = tilesize
        self.margin = margin
        self.mines = int(floor(rows * cols * mine_density))
        self.mines_remaining = self.mines
        self.underboard = [[0 for i in xrange(rows)] for j in xrange(cols)]
        self.rectlist = dict()
        self.gameover = False
        self.firstclick = True
        self.timer_start = 0
        self.timer_task_id = 0

        self._setup()

    ### Public Functions #######################################################
    def reset(self, event=None):
        '''
        Reset the board for another game.
        '''
        self.mines_remaining = self.mines
        self.underboard = [[0 for i in xrange(self.rows)]
                           for j in xrange(self.cols)]
        self.rectlist.clear()
        self.board.delete("all")
        self._setup()
        self.gameover = False
        self.firstclick = True
        self.board.itemconfig(self.mine_counter, text=str(self.mines_remaining))

    ### Private Functions ######################################################
    def _setup(self):
        '''
        Create and ready up the board for play.
        '''
        self._generateMines()
        self._generateGUI()
        self._populateLowerBoard()
        self._populateUpperBoard()
        self._bindBoardEvents()

    def _generateGUI(self):
        self.mine_counter = self.board.create_text(
                                self.cols*self.tilesize,
                                0.5*self.margin_top,
                                font=(None, 20),
                                text=str(self.mines_remaining))
        self.timer = self.board.create_text(
                                1.5*self.margin,
                                0.5*self.margin_top,
                                font=(None, 20),
                                text="{:>6.1f}".format(0),
                                anchor=W)

    def _generateMines(self):
        '''
        Generate mine locations.
        '''
        every_tile = [(i, j) for i in xrange(self.cols)
                             for j in xrange(self.rows)]
        for i in xrange(self.mines):
            coord = every_tile.pop(randint(0, len(every_tile)-1))
            self.underboard[coord[0]][coord[1]] = 9
        del every_tile[:]

    def _populateLowerBoard(self):
        '''
        Fill in the lower level of the board containing the mines and numbers.
        '''
        for col in xrange(self.cols):
            for row in xrange(self.rows):
                if self.underboard[col][row] == 9:
                    self.board.create_rectangle(
                        col*self.tilesize + 2 + self.margin,
                        row*self.tilesize + 2 + self.margin_top,
                        (col+1)*self.tilesize-2 + self.margin,
                        (row+1)*self.tilesize-2 + self.margin_top,
                        fill="black")
                    continue
                # Increment number for each mine in surrounding 8 spaces
                for xs in xrange(-1, 2):
                    for ys in xrange(-1, 2):
                        if col+xs >= 0 and col+xs < self.cols and \
                           row+ys >= 0 and row+ys < self.rows and \
                           self.underboard[col+xs][row+ys] == 9:
                            self.underboard[col][row] += 1
                # Write text on squares
                if self.underboard[col][row] > 0:
                    self.board.create_text(
                        (col+0.5)*self.tilesize + self.margin,
                        (row+0.5)*self.tilesize + self.margin_top,
                        text=str(self.underboard[col][row]))

    def _populateUpperBoard(self):
        '''
        Fill in the upper level of the board containing the clickable squares.
        '''
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                piece = self.board.create_rectangle(
                    i*self.tilesize+self.margin,
                    j*self.tilesize+self.margin_top,
                    (i+1)*self.tilesize+self.margin,
                    (j+1)*self.tilesize+self.margin_top,
                    fill="gray", tags="rect")
                self.rectlist[piece] = (i, j)

    def _clickSquare(self, x, y):
        if self.firstclick:
            self.timer_start = currenttime()
            self._update_timer()
            self.firstclick = False
        self.active_obj = self.board.find_closest(x, y)[0]
        if self.board.itemcget(self.active_obj, "fill") != "red" and \
           self.board.itemcget(self.active_obj, "fill") != "":
           if self.active_obj in self.rectlist:
                self._reveal(self.rectlist[self.active_obj])

    def _flagSquare(self, x, y):
        self.active_obj = self.board.find_closest(x, y)[0]
        if self.board.itemcget(self.active_obj, "fill") == "gray":
            self.board.itemconfigure(self.active_obj, fill="red")
            self.mines_remaining -= 1
        elif self.board.itemcget(self.active_obj, "fill") == "red":
            self.board.itemconfigure(self.active_obj, fill="gray")
            self.mines_remaining += 1
        self.board.itemconfig(self.mine_counter, text=str(self.mines_remaining))
    
    def _reveal(self, loc):
        if loc[0] < 0 or loc[0] >= self.cols or \
           loc[1] < 0 or loc[1] >= self.rows:
            return
        tile = self.underboard[loc[0]][loc[1]]
        if tile < 0:
            return
        elif tile == 9:
            self._lose()
        else:
            self._display(loc)
            if tile == 0:
                for i in xrange(9):
                    newloc = (loc[0]-1 + i%3, loc[1]-1 + i//3)
                    self._reveal(newloc)
    
    def _display(self, loc):
        '''
        Display what's behind a tile.
        '''
        tile = self.board.find_closest(loc[0]*self.tilesize+self.margin,
                                       loc[1]*self.tilesize+self.margin_top)
        if self.board.itemcget(tile, "fill") == "red":
            self.mines_remaining += 1
            self.board.itemconfig(self.mine_counter,
                                  text=str(self.mines_remaining))
        self.board.itemconfigure(tile, fill="")
        self.underboard[loc[0]][loc[1]] = -1

    def _lose(self):
        '''
        Called upon revealing a mine. Ends the game and reveals the board and a
        button to start a new game.
        '''
        self.gameover = True
        self.after_cancel(self.timer_task_id)
        self._drawNewGameButton()
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                self._display((i, j))

    def _drawNewGameButton(self):
        self.board.create_rectangle(
            0.5*self.cols*self.tilesize + self.margin - 60,
            0.5*self.margin_top - 15,
            0.5*self.cols*self.tilesize + self.margin + 60,
            0.5*self.margin_top + 15,
            tags="reset_button",
            fill="grey")
        self.board.create_text(
            0.5*self.cols*self.tilesize + self.margin,
            0.5*self.margin_top,
            font=(None, 18),
            tags="reset_button",
            text="New Game")

    def _update_timer(self):
        self.board.itemconfig(
                self.timer,
                text="{:>6.1f}".format(currenttime() - self.timer_start))
        self.timer_task_id = self.after(100, self._update_timer)

    ### Interaction logic ######################################################
    def _bindBoardEvents(self):
        self.board.tag_bind("rect", "<ButtonPress-1>", self._onMouseDown)
        self.board.tag_bind("rect", "<ButtonRelease-1>", self._onMouseUp)
        self.board.tag_bind("rect", "<ButtonRelease-2>", self._onFlag)
        self.board.tag_bind("reset_button", "<ButtonRelease-1>", self.reset)
        self.bind("<Key>", self._onKeyPress)

    def _onMouseDown(self, event):
        self.active_obj = self.board.find_closest(event.x, event.y)[0]
        if self.board.itemcget(self.active_obj, "fill") != "red" and \
           self.board.itemcget(self.active_obj, "fill") != "":
            self.board.itemconfigure(self.active_obj, fill="dark gray")

    def _onMouseUp(self, event):
        self._clickSquare(event.x, event.y)

    def _onFlag(self, event):
        self._flagSquare(event.x, event.y)

    def _onKeyPress(self, event):
        if self.gameover:
            return
        x = self.winfo_pointerx() + event.x
        y = self.winfo_pointery() + event.y
        if event.char == "a":
            self._clickSquare(x, y)
        elif event.char == "q":
            self._flagSquare(x, y)
