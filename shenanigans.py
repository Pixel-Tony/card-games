import tkinter as tk
import socket
from util import *
import urllib.request

# import os
import asyncio
a = 3
DIR_NAME = '\\'.join(__file__.split('\\')[:-1])
HEIGHTS = {'menu' : 600, 'game' : 800, 'middle': 220}
WIDTHS = {'menu' : 500, 'game' : 1000, 'middle': 500}
TITLE = 'Tony\'s Card Games Catalogue'
CARD_SIZE_MPL = (2, 4)
HEAD_FONT = ("Century Gothic", "14", "bold")
LOW_FONT = HEAD_FONT[0], str(int(HEAD_FONT[1]) - 2), HEAD_FONT[2]

class NameAlreadyInUse(Exception):
    def __init__(self, msg:str) -> None:
        super().__init__(msg)

# class Card():
#     def __init__(self, master, __card_value) -> None:
#         self.rank = __card_value[0]
#         self.suit = __card_value[1]
#         file = DIR_NAME + '\\gfx\\' + str(DECK.index(__card_value)) + '.png'
#         self.image = tk.PhotoImage(master=master, file=file).zoom(CARD_SIZE_MPL[0]).subsample(CARD_SIZE_MPL[1])
#         self.master = master

#     def grid(self, *args, **kwargs):
#         tk.Label(self.master, image=self.image).grid(*args, **kwargs, rowspan=self.image.height(), columnspan=self.image.width())


game_parameters = {'PC' : None, 'Game class' : None, 'Game' : None}

root = tk.Tk()
root.iconphoto(True, tk.PhotoImage(file=DIR_NAME+'/util/logo.png'))
root.geometry(f'{WIDTHS["game"]}x{HEIGHTS["game"]}+{(root.winfo_screenwidth() - WIDTHS["game"])//2}+{(root.winfo_screenheight() - HEIGHTS["game"])//2}')
root.resizable(False, False)
root.withdraw()

__destroy_all = lambda event: root.quit()


__awaiting_players_screen = tk.Toplevel(root)
__awaiting_players_screen.title(TITLE)
__awaiting_players_screen.geometry(f'{WIDTHS["middle"]}x{HEIGHTS["middle"]}+{(root.winfo_screenwidth() - WIDTHS["middle"])//2}+{(root.winfo_screenheight()-HEIGHTS["middle"])//2}')
__awaiting_players_screen.resizable(False, False)
__awaiting_players_screen.withdraw()
__awaiting_players_screen.bind('<Destroy>', __destroy_all)

for column in range(WIDTHS['middle']//10):
    __awaiting_players_screen.grid_columnconfigure(index=int(column), weight=1, minsize=10)
for row in range(HEIGHTS['middle']//10):
    __awaiting_players_screen.grid_rowconfigure(index=int(row), weight=1, minsize=10)




start_menu = tk.Toplevel(root)
start_menu.title(TITLE + ' - Menu')
start_menu.geometry(f'{WIDTHS["menu"]}x{HEIGHTS["menu"]}+{(root.winfo_screenwidth() - WIDTHS["menu"])//2}+{(root.winfo_screenheight() - HEIGHTS["menu"])//2}')
start_menu.resizable(False, False)
start_menu.bind('<Destroy>', __destroy_all)

for column in range(WIDTHS['menu']//10):
    start_menu.grid_columnconfigure(index=int(column), weight=1, minsize=10)
for row in range(HEIGHTS['menu']//10):
    start_menu.grid_rowconfigure(index=int(row), weight=1, minsize=10)

__menu_bg = tk.PhotoImage(file=DIR_NAME + '\gfx\menu_bg.png')
menu_background = tk.Label(start_menu, image=__menu_bg)
menu_background.grid(row=0, column=0, rowspan=60, columnspan=50)


heading_bg = tk.PhotoImage(file=DIR_NAME+'\gfx\heading_bg.png')
heading = tk.Label(start_menu, image=heading_bg, text='Card Games Catalogue'.upper(), font=HEAD_FONT, compound='center', fg='yellow')
heading.grid(row=1, column=1, rowspan=4, columnspan=WIDTHS['menu']//10-2, sticky='WE')

button_host = tk.Button(start_menu, name='button host', text='Host game', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
button_host.grid_configure(row=10, column=16, rowspan=4, columnspan=18, sticky='NESW')

__but_join_game = tk.Button(start_menu, name='button join', text='Join game', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
__but_join_game.grid_configure(row=15, column=16, rowspan=4, columnspan=18, sticky='NESW')

__but_quit_game = tk.Button(start_menu, name='button quit', text='Quit', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
__but_quit_game.grid_configure(row=25, column=16, rowspan=4, columnspan=18, sticky='NESW')

poker_button = tk.Button(start_menu, name='button host poker', text='Poker', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
poker_button.grid_configure(row=10, column=18, rowspan=4, columnspan=14, sticky='NESW')

fool_button = tk.Button(start_menu, name='button host fool', text='Durak', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
fool_button.grid_configure(row=15, column=18, rowspan=4, columnspan=14, sticky='NESW')

game_start_button = tk.Button(start_menu, name='button begin', text='Start', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
game_start_button.grid_configure(row=20, column=18, rowspan=4, columnspan=14, sticky='NESW')

players_counter = tk.Scale(start_menu, orient='horizontal', from_=2, to=8, bg='DeepSkyBlue3', bd=0, font=LOW_FONT, label='Players', activebackground='DeepSkyBlue2')
players_counter.grid_configure(row=10, column=18, rowspan=8, columnspan=14, sticky='NESW')

button_back = tk.Button(start_menu, name='button back to main', text='Back', font=HEAD_FONT, bg='DeepSkyBlue3', activebackground='DeepSkyBlue2')
button_back.grid_configure(row=25, column=18, rowspan=4, columnspan=14, sticky='NESW')

levels:list[list[tk.Button]] = [[button_host, __but_join_game, __but_quit_game], [poker_button, fool_button, button_back], [players_counter, game_start_button, button_back]]




game_parameters = {'PC' : None, # Client - Server
    'Game class' : None, # Poker - Fool
    'Game' : None} # Poker - Omaha

def show_menu(event=None, level=0):
    for elem in __awaiting_players_screen.__dict__['children']:
        __awaiting_players_screen.__dict__['children'][elem].grid_remove()
    for elem in filter(lambda el: not isinstance(root.__dict__['children'][el], tk.Toplevel), root.__dict__['children']):
        root.__dict__['children'][elem].grid_remove()
    __awaiting_players_screen.withdraw()
    root.withdraw()
    [elem.configure(state='normal') for elem in levels[2]]
    [[elem.grid_remove() for elem in level] for level in levels[1:]]
    [elem.grid() for elem in levels[level]]

def __game(__host_or_client):
    def change_level(current_level: int, down: bool=False):
        for widget in levels[current_level]:
            widget.grid_remove()
        current_level += (-1 if down else 1)
        for widget in levels[current_level]:
            widget.grid()
        if current_level >= 1 or not down:
            button_back.configure(command=lambda: change_level(current_level, True))

    def set_player_count(game):
        game_parameters['Game class'] = game
        game_start_button.configure(command=lambda: player_waiting_window('server'))
        button_back.configure(command=lambda: change_level(2, True))
        change_level(1)

    if __host_or_client == 'server':
        change_level(0)
        poker_button.configure(command=lambda: set_player_count('Poker'))
        fool_button.configure(command=lambda: set_player_count('Fool'))
    else:
        player_waiting_window('client')

button_host.configure(command=lambda: __game('server'))
__but_join_game.configure(command=lambda: __game('client'))
__but_quit_game.configure(command=lambda: __destroy_all(None))


def player_waiting_window(pc_type):
    for elem in (levels[2] if pc_type == 'server' else levels[0]):
        elem.configure(state='disabled')
    __awaiting_players_screen.deiconify()

    entry_nickname = tk.Entry(__awaiting_players_screen, font=LOW_FONT)
    entry_nickname.grid(row=2, column=14, rowspan=4, columnspan=16, sticky='NEWS')
    entry_ip_address = tk.Entry(__awaiting_players_screen, font=LOW_FONT)
    tk.Label(__awaiting_players_screen, text='Nickname', font=LOW_FONT, width=2).grid(row=2, column=2, rowspan=4, columnspan=11, sticky='NEWS')
    sock = socket.socket()
    if pc_type == 'server':
        async def connecting_players(sock:socket.socket):
            conn, addr = sock.accept()
            p_name = conn.recv(1024).decode().capitalize()
            while p_name in client_connections.keys():
                conn.send('failure'.encode())
                p_name = conn.recv(1024).decode().capitalize()
            client_connections[p_name] = {'connection' : conn, 'address' : addr}
            join_button.configure(state='normal')

        game_parameters['Player count'] = players_counter.get()


        join_button = tk.Button(__awaiting_players_screen, text='Join', font=HEAD_FONT, state='disabled')
        join_button.grid(row=2, column=31, rowspan=4, columnspan=8, sticky='NEWS')

        tk.Button(__awaiting_players_screen, text='Back', font=HEAD_FONT, command=lambda: show_menu(level=2)).grid(row=2, column=40, rowspan=4, columnspan=8, sticky='NEWS')

        lines = f'Your IP-address is {urllib.request.urlopen("https://ident.me").read().decode("utf8")}'
        lines += '\n * Tell your friends to connect to this IP-adress;'
        lines += '\n * Make sure the 50240 port is open.'
        lines += '\n\nWhen all the friends connect, hit "Join" to start'
        tk.Label(__awaiting_players_screen, text=lines, font=LOW_FONT, justify='left', wraplength=460).grid(row=7, column=2, rowspan=20, columnspan=46, sticky='NEWS')

        client_connections = {}
        sock.bind(('', 50240))
        sock.listen(game_parameters['Player count'])

        #TODO:

    elif pc_type == 'client':
        entry_ip_address.grid(row=7, column=14, rowspan=4, columnspan=16, sticky="NEWS")


        tk.Label(__awaiting_players_screen, text='IP-Address', font=LOW_FONT).grid(row=7, column=2, rowspan=4, columnspan=11, sticky='NEWS')






        #TODO:

show_menu()

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

