import tkinter as tk
import socket
from typing import Type
from util import *
from urllib.request import urlopen
import asyncio
from _tkinter import TclError

DIR_NAME = '\\'.join(__file__.split('\\')[:-1])
DIMS = {'menu': (500, 600), 'middle': (500, 220), 'game' : (1000, 800)}
TITLE = 'Tony\'s Card Games Catalogue'
CARD_SIZE_MPL = (2, 4)
HEAD_FONT = ("Century Gothic", "14", "bold")
LOW_FONT = HEAD_FONT[0], str(int(HEAD_FONT[1]) - 2), HEAD_FONT[2]

game_parameters = {
    'Server' : None,   # Client - Server
    'Game' : None,     # Poker - Fool
    'Variation' : None # Poker - Omaha
}


class Window:
    class sheet:
        def __init__(self, *items:tk.Widget) -> None:
            self.collection = items

        def hide(self):
            [elem.grid_remove() for elem in self.collection]

        def show(self):
            [elem.grid() for elem in self.collection]

        def disable(self):
            [elem.configure(state='disabled') for elem in self.collection]

        def enable(self):
            [elem.configure(state='normal') for elem in self.collection]

    def __init__(self, name:str, title, parent:'Window'=None) -> None:
        self.name = name
        self.sheets = dict()
        self.size = DIMS[name]
        self.win = tk.Tk()
        self.parent = parent if parent != None else self
        self.win.bind('<Destroy>', lambda *args: self.win.quit())
        self.win.resizable(0, 0)
        self.win.title(title)
        a, b = (self.win.winfo_screenwidth() - self.size[0])//2, (self.win.winfo_screenheight() - self.size[1])//2
        self.win.geometry(f'{self.size[0]}x{self.size[1]}+{a}+{b}')

        for row in range(self.size[1] // 10):
            self.win.rowconfigure(row, weight=1, minsize=10)
        for column in range(self.size[0] // 10):
            self.win.columnconfigure(column, weight=1, minsize=10)
        self.hide()

    def sheet_add(self, id, *items):
        new_sheet = self.sheet(*items)
        self.sheets = dict([*self.sheets.items(), (id, new_sheet)])
        self.sheets[id].hide()

    def sheet_show(self, id):
        for sh in self.sheets:
            self.sheets[sh].hide()
        self.sheets[id].show()

    def hide(self):
        self.win.withdraw()

    def show(self, id=None):
        self.win.deiconify()
        if id != None:
            self.sheets[id].show()

    def mainloop(self):
        self.win.mainloop()


# class Card():
#     def __init__(self, master, __card_value) -> None:
#         self.rank = __card_value[0]
#         self.suit = __card_value[1]
#         file = DIR_NAME + '\\gfx\\' + str(DECK.index(__card_value)) + '.png'
#         self.image = tk.PhotoImage(master=master, file=file).zoom(CARD_SIZE_MPL[0]).subsample(CARD_SIZE_MPL[1])
#         self.master = master

#     def grid(self, *args, **kwargs):
#         tk.Label(self.master, image=self.image).grid(*args, **kwargs, rowspan=self.image.height(), columnspan=self.image.width())


# Initialising all windows
root = Window('game', TITLE)
start_menu = Window('menu', TITLE, root)
__awaiting_players_screen = Window('middle', TITLE, root)

icon_pic = tk.PhotoImage(master=root.win, file=DIR_NAME+'/util/logo.png')
root.win.iconphoto(True, icon_pic)

# First window - main menu
# Adding the stuff that will be always visible
__menu_bg = tk.PhotoImage(master=start_menu.win, file=DIR_NAME + '\gfx\menu_bg.png')
__heading_bg = tk.PhotoImage(master=start_menu.win, file=DIR_NAME+'\gfx\heading_bg.png')

menu_background = tk.Label(start_menu.win, image=__menu_bg)
heading = tk.Label(start_menu.win, image=__heading_bg, text='Card Games Catalogue'.upper(), font=HEAD_FONT, compound='center', fg='yellow')
button_back = tk.Button(start_menu.win, text='Back', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')

menu_background.grid(row=0, column=0, rowspan=60, columnspan=50, sticky='NEWS')
heading.grid(row=1, column=1, rowspan=4, columnspan=48, sticky='WE')
button_back.grid(row=25, column=18, rowspan=4, columnspan=14, sticky='NESW')

# Adding first sheet - start menu
button_host_game = tk.Button(start_menu.win, text='Host game', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
button_join_game = tk.Button(start_menu.win, text='Join game', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
button_quit_game = tk.Button(start_menu.win, text='Quit', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')

button_host_game.grid(row=10, column=16, rowspan=4, columnspan=18, sticky='NESW')
button_join_game.grid(row=15, column=16, rowspan=4, columnspan=18, sticky='NESW')
button_quit_game.grid(row=25, column=16, rowspan=4, columnspan=18, sticky='NESW')

start_menu.sheet_add(0, button_host_game, button_join_game, button_quit_game)

# Adding second sheet - game choose
button_poker = tk.Button(start_menu.win, text='Poker', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
button_durak = tk.Button(start_menu.win, text='Durak', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')

button_poker.grid(row=10, column=18, rowspan=4, columnspan=14, sticky='NESW')
button_durak.grid(row=15, column=18, rowspan=4, columnspan=14, sticky='NESW')

start_menu.sheet_add(1, button_poker, button_durak)

# Adding third sheet - player count and start
game_start_button = tk.Button(start_menu.win, text='Start', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
players_counter = tk.Scale(start_menu.win, orient='horizontal', from_=2, to=8, bg='DeepSkyBlue3', bd=0, font=LOW_FONT, label='Players', activebackground='DeepSkyBlue2')

game_start_button.grid(row=20, column=18, rowspan=4, columnspan=14, sticky='NESW')
players_counter.grid(row=10, column=18, rowspan=8, columnspan=14, sticky='NESW')

start_menu.sheet_add(2, game_start_button, players_counter)

# Second window - player nickname choose
entry_nickname = tk.Entry(__awaiting_players_screen.win, font=LOW_FONT)
entry_nickname.grid(row=2, column=14, rowspan=4, columnspan=16, sticky='NEWS')
tk.Label(__awaiting_players_screen.win, text='Nickname', font=LOW_FONT, width=2).grid(row=2, column=2, rowspan=4, columnspan=11, sticky='NEWS')

# Adding first sheet - server
button_join = tk.Button(__awaiting_players_screen.win, text='Join', font=HEAD_FONT, state='disabled')
button_back_to_menu = tk.Button(__awaiting_players_screen.win, text='Back', font=HEAD_FONT)
__lines = f'''Your IP-address is {urlopen("https://ident.me").read().decode("utf8")}
* Tell Your friends to connect to this IP-address
* Make sure the 50240 port is open
\n When all the players connect, hit "Join" to start'''
text_server = tk.Label(__awaiting_players_screen.win, text=__lines, font=LOW_FONT, justify='left', wraplength=460)

button_back_to_menu.grid(row=2, column=40, rowspan=4, columnspan=8, sticky='NEWS')
text_server.grid(row=7, column=2, rowspan=20, columnspan=46, sticky='NEWS')
button_join.grid(row=2, column=31, rowspan=4, columnspan=8, sticky='NEWS')

__awaiting_players_screen.sheet_add(0, button_back_to_menu, text_server, button_join)

# Adding second sheet - client
entry_ip_address = tk.Entry(__awaiting_players_screen.win, font=LOW_FONT)
label_address = tk.Label(__awaiting_players_screen.win, text='IP-Address', font=LOW_FONT)
entry_ip_address.grid(row=7, column=14, rowspan=4, columnspan=16, sticky="NEWS")
label_address.grid(row=7, column=2, rowspan=4, columnspan=11, sticky='NEWS')

__awaiting_players_screen.sheet_add(1, entry_ip_address, label_address)







def temp():
    async def connecting_players(sock:socket.socket):
        conn, addr = sock.accept()
        p_name = conn.recv(1024).decode().capitalize()
        while p_name in client_connections.keys():
            conn.send('failure'.encode())
            p_name = conn.recv(1024).decode().capitalize()
        client_connections[p_name] = {'connection' : conn, 'address' : addr}
        button_join.configure(state='normal')

    game_parameters['Player count'] = players_counter.get()
    sock = socket.socket()
    client_connections = {}
    sock.bind(('', 50240))
    sock.listen(game_parameters['Player count'])









start_menu.show(0)
__awaiting_players_screen.show(0)

root.mainloop()
