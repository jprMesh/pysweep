from math import floor
from random import randint

class Mineboard:
    def __init__(self, 
                 board,
                 mine_density = 0.15,
                 rows = 20,
                 cols = 30,
                 tilesize = 20,
                 margin_width = 20,
                 margin_height = 20):

        self.board = board

        self.rows = rows
        self.cols = cols
        self.tilesize = tilesize
        self.margin_width = margin_width
        self.margin_height = margin_height
        
        self.playboard = [[0 for i in range(rows)] for j in range(cols)]
        self.rectlist = dict()
        
        # Populate board with mines
        # O(inf) time complexity
        totalmines = floor(rows*cols*mine_density)
        self.mines = 0
        while self.mines < totalmines:
            mine_coord = (randint(0, self.cols-1), randint(0, self.rows-1))
            if self.playboard[mine_coord[0]][mine_coord[1]] == 9:
                continue
            self.playboard[mine_coord[0]][mine_coord[1]] = 9
            self.mines += 1

    def populateBoard(self):
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                if self.playboard[i][j] == 9:
                    self.board.create_rectangle(i*self.tilesize+2+self.margin_width, j*self.tilesize+2+self.margin_height,
                                           (i+1)*self.tilesize-2+self.margin_width, (j+1)*self.tilesize-2+self.margin_height,
                                           fill="black")
                    continue
                for xs in xrange(-1, 2):
                    for ys in xrange(-1, 2):
                        if i+xs >= 0 and j+ys >= 0 and i+xs < self.cols and j+ys < self.rows:
                            if self.playboard[i+xs][j+ys] == 9:
                                self.playboard[i][j] += 1
                if self.playboard[i][j] > 0:
                    self.board.create_text((i+0.5)*self.tilesize+self.margin_width, (j+0.5)*self.tilesize+self.margin_height,
                                      text=str(self.playboard[i][j]))
        # Why does this loop increment by tilesize while the previous loop increments by 1????
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                piece = self.board.create_rectangle(i*self.tilesize+2+self.margin_width, j*self.tilesize+2+self.margin_height,
                                               (i+1)*self.tilesize-2+self.margin_width, (j+1)*self.tilesize-2+self.margin_height,
                                               fill="gray", tags="rect")
                self.rectlist[piece] = (i, j)

    def onObjectClick(self, event):
        board_loc = event.widget.find_closest(event.x, event.y)[0]
        if self.board.itemcget(board_loc, "fill") != "red":
            self.reveal(self.rectlist[board_loc])

    def flag(self, event):
        board_loc = event.widget.find_closest(event.x, event.y)[0]
        if self.board.itemcget(board_loc, "fill") == "gray":
            self.board.itemconfigure(board_loc, fill="red")
        else:
            self.board.itemconfigure(board_loc, fill="gray")

    def bindBoardEvents(self):
        self.board.tag_bind("rect", "<ButtonPress-1>", self.onObjectClick)
        self.board.tag_bind("rect", "<ButtonPress-2>", self.flag)

    def lose(self):
        print "you lose"
        for i in xrange(self.cols):
            for j in xrange(self.rows):
                self.display((i, j))
    
    def reveal(self, loc):
        if loc[0] < 0 or loc[1] < 0 or loc[0] >= self.cols or loc[1] >= self.rows:
            return
        tile = self.playboard[loc[0]][loc[1]]
        if tile < 0:
            return
        elif tile == 9:
            self.lose()
        elif tile == 0:
            self.display(loc)
            for i in xrange(9):
                newloc = (loc[0]-1 + i%3, loc[1]-1 + i//3)
                self.reveal(newloc)
        else:
            self.display(loc)
    
    def display(self, loc):
        tile = self.board.find_closest(loc[0]*self.tilesize+self.margin_width, loc[1]*self.tilesize+self.margin_height)
        self.board.itemconfigure(tile, fill="")
        self.playboard[loc[0]][loc[1]] = -1

