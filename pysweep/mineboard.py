from Tkinter import *
from math import floor
from random import randint

class Mineboard(Frame):
    def __init__(self,
                 mine_density = 0.15,
                 rows = 20,
                 cols = 30,
                 tilesize = 20,
                 margin = 20):

        Frame.__init__(self)
        self.grid(row=0, column=0)
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

        self._setup()

    def _setup(self):
        '''
        Create and ready up the board for play.
        '''
        self._generateMines()
        self._generateGUI()
        self._populateLowerBoard()
        self._populateUpperBoard()
        self._bindBoardEvents()

    def reset(self):
        '''
        Reset the board for another game.
        '''
        self.mines_remaining = self.mines
        self.underboard[:] = 0
        self.rectlist.clear()
        self._setup()

    def _generateGUI(self):
        self.mine_counter = self.board.create_text(
                                self.cols*self.tilesize,
                                0.5*self.margin_top,
                                font=(None, 20),
                                text=str(self.mines_remaining))

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

    def _onClick(self, event):
        self.active_obj = event.widget.find_closest(event.x, event.y)[0]
        if self.board.itemcget(self.active_obj, "fill") != "red" and \
           self.board.itemcget(self.active_obj, "fill") != "":
            self.board.itemconfigure(self.active_obj, fill="dark gray")

    def _onRelease(self, event):
        if self.board.itemcget(self.active_obj, "fill") != "red" and \
           self.board.itemcget(self.active_obj, "fill") != "":
            self._reveal(self.rectlist[self.active_obj])

    def _onFlag(self, event):
        board_loc = event.widget.find_closest(event.x, event.y)[0]
        if self.board.itemcget(board_loc, "fill") == "gray":
            self.board.itemconfigure(board_loc, fill="red")
            self.mines_remaining -= 1
        elif self.board.itemcget(board_loc, "fill") == "red":
            self.board.itemconfigure(board_loc, fill="gray")
            self.mines_remaining += 1
        self.board.itemconfig(self.mine_counter, text=str(self.mines_remaining))

    def _bindBoardEvents(self):
        self.board.tag_bind("rect", "<ButtonPress-1>", self._onClick)
        self.board.tag_bind("rect", "<ButtonRelease-1>", self._onRelease)
        self.board.tag_bind("rect", "<ButtonRelease-2>", self._onFlag)

    def _lose(self):
        print "you lose"
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                self._display((i, j))
    
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
        tile = self.board.find_closest(loc[0]*self.tilesize+self.margin,
                                       loc[1]*self.tilesize+self.margin_top)
        self.board.itemconfigure(tile, fill="")
        self.underboard[loc[0]][loc[1]] = -1
