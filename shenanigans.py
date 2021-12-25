import tkinter as tk
from tkinter.constants import S
from util.poker_util import ORDER, DECK, SUITS, SPADE




DIR_NAME = '\\'.join(__file__.split('\\')[:-1])
WIDTH = 1000
HEIGHT = 800

HEAD_FONT = "Century Gothic", "12", "bold"
LOW_FONT = "Century Gothic", "11", "bold"

class CardPic():
    def __init__(self, master, __card_value) -> None:
        self.rank = __card_value[0]
        self.suit = __card_value[1]
        file = DIR_NAME + '\\gfx\\'
        file += str(([*range(2,11), 'Jack', 'Queen', 'King', 'Ace'])[ORDER.index(self.rank)])
        file += ' of ' + {'♠' : 'Spades', '♥' : 'Hearts', '♣' : 'Clubs', '♦' : 'Diamonds'}[self.suit]
        file += '.png'

        self.image = tk.PhotoImage(master=master, file=file)
        self.master = master
        self.image = self.image.zoom(20).subsample(25)

    def grid(self, *args, **kwargs):
        tk.Label(self.master, image=self.image).grid(*args, **kwargs)





root = tk.Tk()
root.title('Tony\'s Card Games Catalogue')
root.geometry(f'{WIDTH}x{HEIGHT}+{(root.winfo_screenwidth() - WIDTH)//2}+{(root.winfo_screenheight() - HEIGHT)//2}')
root.resizable(False, False)
root.iconphoto(True, tk.PhotoImage(file=DIR_NAME+'/util/logo.png'))



card = CardPic(root, ('J', SPADE), (DIR_NAME+'/util/spade jack.png'))
card.grid()

tk.LabelFrame(root, bg='black', border=2).grid()

root.mainloop()




# from tkinter import *
# def hello(event):
#     print("Single Click, Button-l")
# def quit(event):
#     print("Double Click, so let's stop")
#     import sys; sys.exit()

# widget = Button(None, text='Mouse Clicks')
# widget.pack()
# widget.bind('<Button-1>', hello)
# widget.bind('<Double-1>', quit)
# widget.mainloop()
