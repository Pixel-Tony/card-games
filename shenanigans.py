import tkinter as tk
from typing import Union
# import time
# import socket
from util import *
# import urllib.request
# import os


DIR_NAME = '\\'.join(__file__.split('\\')[:-1])

HEIGHTS = {'menu' : 600, 'game' : 800, 'middle': 200}
WIDTHS = {'menu' : 500, 'game' : 1000, 'middle': 300}
TITLE = 'Tony\'s Card Games Catalogue'
CARD_SIZE_MPL = (2, 4)
HEAD_FONT = ("Century Gothic", "14", "bold")
LOW_FONT = HEAD_FONT[0], str(int(HEAD_FONT[1]) - 1), HEAD_FONT[2]

class Card():
    def __init__(self, master, __card_value) -> None:
        self.rank = __card_value[0]
        self.suit = __card_value[1]
        file = DIR_NAME + '\\gfx\\' + str(DECK.index(__card_value)) + '.png'
        self.image = tk.PhotoImage(master=master, file=file).zoom(CARD_SIZE_MPL[0]).subsample(CARD_SIZE_MPL[1])
        self.master = master

    def grid(self, *args, **kwargs):
        tk.Label(self.master, image=self.image).grid(*args, **kwargs, rowspan=self.image.height(), columnspan=self.image.width())


game_parameters = {'PC' : None, 'game_class' : None, 'game' : None}
main_game = tk.Tk()
main_game.iconphoto(True, tk.PhotoImage(file=DIR_NAME+'/util/logo.png'))
main_game.geometry(f'{WIDTHS["game"]}x{HEIGHTS["game"]}+{(main_game.winfo_screenwidth() - WIDTHS["game"])//2}+{(main_game.winfo_screenheight() - HEIGHTS["game"])//2}')
main_game.resizable(False, False)
main_game.withdraw()



start_menu = tk.Toplevel(main_game)
start_menu.title(TITLE + ' - Menu')
start_menu.geometry(f'{WIDTHS["menu"]}x{HEIGHTS["menu"]}+{(main_game.winfo_screenwidth() - WIDTHS["menu"])//2}+{(main_game.winfo_screenheight() - HEIGHTS["menu"])//2}')
start_menu.resizable(False, False)

__awaiting_players_screen = tk.Toplevel(main_game)
__awaiting_players_screen.title(TITLE)
__awaiting_players_screen.geometry(f'{WIDTHS["middle"]}x{HEIGHTS["middle"]}+{(main_game.winfo_screenwidth() - WIDTHS["middle"])//2}+{(main_game.winfo_screenheight()-HEIGHTS["middle"])//2}')
__awaiting_players_screen.withdraw()




for column in range(WIDTHS['menu']//10):
    start_menu.grid_columnconfigure(index=int(column), weight=1, minsize=10)
for row in range(HEIGHTS['menu']//10):
    start_menu.grid_rowconfigure(index=int(row), weight=1, minsize=10)
__menu_bg = tk.PhotoImage(file=DIR_NAME + '\gfx\\menu_bg.png')
menu_background = tk.Label(start_menu, image=__menu_bg)
menu_background.grid(row=0, column=0, rowspan=60, columnspan=50)

heading_bg = tk.PhotoImage(file=DIR_NAME+'\gfx\heading_bg.png')
heading = tk.Label(start_menu, image=heading_bg, text='Card Games Catalogue'.upper(), font=HEAD_FONT, compound='center', fg='yellow')
heading.grid(row=1, column=1, rowspan=4, columnspan=WIDTHS['menu']//10-2, sticky='WE')

__but_host_game = tk.Button(start_menu, name='button host', text='Host game', font=HEAD_FONT, bg='cyan3', activebackground='cyan2')
__but_host_game.grid_configure(row=10, column=16, rowspan=4, columnspan=18, sticky='NESW')

__but_join_game = tk.Button(start_menu, name='button join', text='Join game', font=HEAD_FONT, bg='cyan3', activebackground='cyan2')
__but_join_game.grid_configure(row=15, column=16, rowspan=4, columnspan=18, sticky='NESW')

__but_quit_game = tk.Button(start_menu, name='button quit', text='Quit', font=HEAD_FONT, bg='cyan3', activebackground='cyan2')
__but_quit_game.grid_configure(row=25, column=16, rowspan=4, columnspan=18, sticky='NESW')

poker_button = tk.Button(start_menu, name='button host poker', text='Poker', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
poker_button.grid_configure(row=10, column=18, rowspan=4, columnspan=14, sticky='NESW')

fool_button = tk.Button(start_menu, name='button host fool', text='Durak', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
fool_button.grid_configure(row=15, column=18, rowspan=4, columnspan=14, sticky='NESW')

game_start_button = tk.Button(start_menu, name='button begin', text='Start', font=HEAD_FONT, bg='DodgerBlue3', activebackground='Dodgerblue2')
game_start_button.grid_configure(row=20, column=18, rowspan=4, columnspan=14, sticky='NESW')

players_counter = tk.Scale(start_menu, orient='horizontal', from_=2, to=8, bg='DodgerBlue3', fg='yellow', bd=1, font=LOW_FONT, label='Player count', activebackground='DodgerBlue4')
players_counter.grid_configure(row=10, column=18, rowspan=8, columnspan=14, sticky='NESW')

button_back = tk.Button(start_menu, name='button back to main', text='Back', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
button_back.grid_configure(row=25, column=18, rowspan=4, columnspan=14, sticky='NESW')

levels = [[__but_host_game, __but_join_game, __but_quit_game], [poker_button, fool_button, button_back], [players_counter, game_start_button, button_back]]

def main(event=None):
    [[elem.grid_remove() for elem in level] for level in levels[1:]]
    [elem.grid() for elem in levels[0]]
    [elem.configure(state='active') for elem in levels[2]]

def __game(__host_or_client):
    def change_level(current_level:int, down:bool=False):
        for widget in levels[current_level]:
            widget.grid_remove()
        current_level += (-1 if down else 1)
        for widget in levels[current_level]:
            widget.grid()
        if current_level >= 1 or not down:
            button_back.configure(command=lambda: change_level(current_level, True))

    def start_game():
        game_parameters['Player count'] = players_counter.get()
        # start_menu.withdraw()
        for elem in levels[2]:
            elem.configure(state='disabled')
        __awaiting_players_screen.deiconify()


    def set_game_type():
        def set_player_count(game:str):
            game_parameters['game_class'] = game
            game_start_button.configure(command=start_game)
            button_back.configure(command=lambda: change_level(2, True))
            change_level(1)

        change_level(0)
        button_back.configure(command=lambda: change_level(1, True))
        poker_button.configure(command=lambda: set_player_count('Poker'))
        fool_button.configure(command=lambda: set_player_count('Fool'))


    if __host_or_client == 'host':
        set_game_type()



__but_host_game.configure(command=lambda: __game('host'))





__destroy = lambda event: main_game.quit()
__but_quit_game.configure(command=lambda: __destroy(None))
start_menu.bind('<Destroy>', __destroy)
__awaiting_players_screen.bind('<Destroy>', __destroy)

main()
main_game.mainloop()

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
