from Tkinter import *

class Menu(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid(row=0, column=0, sticky=N+S+E+W)

        play_button = Button(self, text="Play", command=self.switchToGame)
        play_button.pack()

    def switchToGame(self):
        self.lower()