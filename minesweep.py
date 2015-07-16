from Tkinter import *
from random import randint

def onObjectClick(event):
    board_loc = event.widget.find_closest(event.x, event.y)[0]
    if board.itemcget(board_loc, "fill") != "red":
        reveal(rectlist[board_loc])

def flag(event):
    board_loc = event.widget.find_closest(event.x, event.y)[0]
    if board.itemcget(board_loc, "fill") == "gray":
        board.itemconfigure(board_loc, fill="red")
    else:
        board.itemconfigure(board_loc, fill="gray")

def lose():
    print "you lose"
    for i in xrange(1, rows+1):
        for j in xrange(1, cols+1):
            display(i, j)

def reveal(tuple_loc):
    x, y = tuple_loc
    if playboard[x][y] < 0:
        return
    elif playboard[x][y] == 9:
        lose()
    elif playboard[x][y] == 0:
        if x != 0 and y != 0 and x != rows+1 and y != cols+1:
            display(x,y)
            for i in xrange(9):
                newloc = (x-1 + i%3, y-1 + i//3)
                reveal(newloc)
    else:
        display(x,y)

def display(x, y):
    loc = board.find_closest(x*tilesize, y*tilesize)
    board.itemconfigure(loc, fill="")
    playboard[x][y] = -1

if __name__ == "__main__":
    rows = 30
    cols = 20
    tilesize = 20
    totalmines = rows*cols*0.15

    root = Tk()
    board = Canvas(root, width=tilesize*rows+40, height=tilesize*cols+40)
    rectlist = dict()
    playboard = [[0 for x in range(cols+2)] for x in range(rows+2)]
    
    mines = 0
    while mines < totalmines:
        xmine = randint(1,rows)
        ymine = randint(1,cols)
        if playboard[xmine][ymine] == 9:
            continue
        playboard[xmine][ymine] = 9
        mines += 1

    for i in xrange(1, rows+1):
        for j in xrange(1, cols+1):
            if playboard[i][j] == 9:
                board.create_rectangle(i*tilesize+2, j*tilesize+2,
                                       (i+1)*tilesize-2, (j+1)*tilesize-2,
                                       fill="black")
                continue
            for xs in xrange(-1, 2):
                for ys in xrange(-1, 2):
                    if playboard[i+xs][j+ys] == 9:
                        playboard[i][j] += 1
            if playboard[i][j] > 0:
                board.create_text((i+0.5)*tilesize, (j+0.5)*tilesize,
                                  text=str(playboard[i][j]))

    for xinit in xrange(20, tilesize*rows+1, tilesize):
        for yinit in xrange(20, tilesize*cols+1, tilesize):
            piece = board.create_rectangle(xinit, yinit, xinit+tilesize,
                                           yinit+tilesize, fill="gray",
                                           tags="rect")
            rectlist[piece] = (xinit/tilesize, yinit/tilesize)

    board.tag_bind("rect", "<ButtonPress-1>", onObjectClick)
    board.tag_bind("rect", "<ButtonPress-2>", flag)
    board.pack()
    root.mainloop()
