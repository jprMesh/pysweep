from Tkinter import *
from math import floor
from random import randint

class Mineboard(Frame):
    def __init__(self,
                 mine_density = 0.15,
                 rows = 20,
                 cols = 30,
                 tilesize = 20,
                 margin_width = 20,
                 margin_height = 20):

        Frame.__init__(self)
        self.grid(row=0, column=0)
        self.board = Canvas(self,
                            width = 2*margin_width + cols*tilesize,
                            height = 2*margin_height + rows*tilesize)
        self.board.pack()

        self.rows = rows
        self.cols = cols
        self.tilesize = tilesize
        self.margin_width = margin_width
        self.margin_height = margin_height
        self.mines = int(floor(rows * cols * mine_density))
        
        self.underboard = [[0 for i in xrange(rows)] for j in xrange(cols)]
        self.rectlist = dict()

        self._setup()

    def _setup(self):
        '''
        Create and ready up the board for play.
        '''
        self._generateMines()
        self._populateLowerBoard()
        self._populateUpperBoard()
        self._bindBoardEvents()

    def reset(self):
        '''
        Reset the board for another game.
        '''
        self.underboard[:] = 0
        self.rectlist.clear()
        self._setup()

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
                        col*self.tilesize+2+self.margin_width,
                        row*self.tilesize+2+self.margin_height,
                        (col+1)*self.tilesize-2+self.margin_width,
                        (row+1)*self.tilesize-2+self.margin_height,
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
                        (col+0.5)*self.tilesize + self.margin_width,
                        (row+0.5)*self.tilesize + self.margin_height,
                        text=str(self.underboard[col][row]))

    def _populateUpperBoard(self):
        '''
        Fill in the upper level of the board containing the clickable squares.
        '''
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                piece = self.board.create_rectangle(
                    i*self.tilesize+self.margin_width,
                    j*self.tilesize+self.margin_height,
                    (i+1)*self.tilesize+self.margin_width,
                    (j+1)*self.tilesize+self.margin_height,
                    fill="gray", tags="rect")
                self.rectlist[piece] = (i, j)

    def onObjectActive(self, event):
        self.active_obj = event.widget.find_closest(event.x, event.y)[0]
        if self.board.itemcget(self.active_obj, "fill") != "red" and \
           self.board.itemcget(self.active_obj, "fill") != "":
            self.board.itemconfigure(self.active_obj, fill="dark gray")

    def onObjectClick(self, event):
        if self.board.itemcget(self.active_obj, "fill") != "red" and \
           self.board.itemcget(self.active_obj, "fill") != "":
            self._reveal(self.rectlist[self.active_obj])

    def _flag(self, event):
        board_loc = event.widget.find_closest(event.x, event.y)[0]
        if self.board.itemcget(board_loc, "fill") == "gray":
            self.board.itemconfigure(board_loc, fill="red")
        elif self.board.itemcget(board_loc, "fill") == "red":
            self.board.itemconfigure(board_loc, fill="gray")

    def _bindBoardEvents(self):
        self.board.tag_bind("rect", "<ButtonPress-1>", self.onObjectActive)
        self.board.tag_bind("rect", "<ButtonRelease-1>", self.onObjectClick)
        self.board.tag_bind("rect", "<ButtonRelease-2>", self._flag)

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
        tile = self.board.find_closest(loc[0]*self.tilesize+self.margin_width,
                                       loc[1]*self.tilesize+self.margin_height)
        self.board.itemconfigure(tile, fill="")
        self.underboard[loc[0]][loc[1]] = -1

