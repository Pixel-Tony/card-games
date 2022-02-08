# import os.path
# import threading
# import tkinter as tk
# from tkinter import font
# import socket
# import select
# from util import *
# import json

# IP, PORT = get_ip(), 50240
# DIR = '\\'.join(__file__.split('\\')[:-1])
# TITLE = 'Tony\'s Card Games Catalogue'
# DIMS = {
#     'menu': (500, 600),
#     'middle': (500, 130),
#     'game' : (1200, 800)
# }
# game_parameters = {
#     'Server' : None,          # Client - Server
#     'Game' : None,            # Poker - Durak
#     'Variation' : None,       # Poker - Omaha
#     'Player count' : None     # 2 - 8
# }
# class Params:
#     color_white = '#fff'
#     color_light_grey = '#e0f0e0'
#     color_grey = '#aaa'
#     color_warning = '#fe1'
#     color_BG = '#484'
#     color_black = '#101010'
#     color_dark_blue = '#002030'
#     color_gold = '#ff3'

#     _font = "Century Gothic"
#     font_head = _font, "14", "bold"
#     FONT_MIDDLE = _font, "12", "bold"
#     FONT_LOW = _font, "11", "bold"


# if os.path.exists(DIR + r'\util\player.json'):
#     player_parameters: dict[str, Union[str, None]] = json.load(open(DIR + r'\util\player.json'), 'r')
# else:
#     player_parameters = {'Name' : '', 'IP' : ''}




# cnf_menu_button = {'font' : Params.font_head, 'bg' : 'DeepSkyBlue3', 'activebackground' : 'DeepSkyBlue2'}
# cnf_lbl = {'bg' : Params.color_BG, 'fg' : 'white'}
# cnf_lbl_g = {'rowspan' : 4, 'sticky' : "NEWS"}

# class GameCode:
#     def __init__(self, ind: int, exception: Exception = None) -> None:
#         self.ind = ind
#         self.exception = exception() if exception else None
#         self.is_ok = (exception == None)

#     def __eq__(self, target: 'GameCode'): return self.ind == target.ind

# class NameExistsError(Exception):
#     def __init__(self) -> None:
#         Exception().__init__('Name is currently in use in this lobby')

# class GameClosedError(Exception):
#     def __init__(self) -> None:
#         Exception().__init__('Connection closed by host')

# class BoolTrigger:
#     instances: list['BoolTrigger'] = []

#     def __init__(self, state = False) -> None:
#         self.state = bool(state)
#         BoolTrigger.instances += [self]

#     def __bool__(self) -> bool:
#         return self.state

#     def __repr__(self) -> str: # just in case
#         return f"<BoolTrigger, state={self.state}>"

#     def toggle(self): self.state = not self.state

#     @classmethod
#     def disable(cls):
#         '''Tkinter-specific, put all instances' states to 1'''
#         for i in cls.instances:
#             i.state = True

# class Window:
#     class _sheet:
#         def __init__(self, *items:tk.Widget) -> None:
#             self.collection: list[tk.Widget] = poker_util.reduce(lambda res, a: res + [a] if not isinstance(a, list) else res + a, items, [])

#         def hide(self): [elem.grid_remove() for elem in self.collection]
#         def show(self): [elem.grid() for elem in self.collection]
#         def disable(self): [elem.configure(state='disabled') for elem in self.collection]
#         def enable(self): [elem.configure(state='normal') for elem in self.collection]

#     def __init__(self, name: str, title: str, master: 'Window' = ..., bg: str = None) -> None:
#         Sheet = self._sheet
#         self._sheets: dict[Union[int, str], Sheet] = dict()
#         self._size = DIMS[name]
#         self.win = tk.Tk() if master == ... else tk.Toplevel(master.win)
#         self.win.protocol("WM_DELETE_WINDOW", lambda: BoolTrigger.disable() or start_menu.win.destroy())
#         self.win.resizable(0, 0)
#         self.win.title(title)
#         a, b = (self.win.winfo_screenwidth() - self._size[0]) // 2, (self.win.winfo_screenheight() - self._size[1]) // 2
#         self._geometry = f'{self._size[0]}x{self._size[1]}+{a}+{b}'
#         self.win.geometry(self._geometry)
#         self.current_sheet = 0
#         if bg != None: self.win['bg'] = bg
#         self._hidden: bool = False

#         for column in range(self._size[0] // 10):
#             self.win.columnconfigure(column, weight=1, minsize=10)
#         for row in range(self._size[1] // 10):
#             self.win.rowconfigure(row, weight=1, minsize=10)
#         self.hide()

#     def add_sheet(self, id:Union[int, str], *items):
#         self._sheets[id] = self._sheet(*items)
#         self._sheets[id].hide()

#     def show_sheet(self, id):
#         for sh in self._sheets:
#             self._sheets[sh].hide()
#         self._sheets[id].show()

#     def hide(self):
#         self.win.withdraw()
#         self._hidden = True

#     def show(self, ind):
#         if self._hidden:
#             self.win.geometry(self._geometry)
#             self._hidden = not self._hidden
#         [self._sheets[sh].hide() for sh in self._sheets]
#         self._sheets[ind].show()
#         self.current_sheet = ind
#         self.win.deiconify()

#     def mainloop(self): self.win.mainloop()

#     def enable_debug(self):
#         row = lambda e: int((e.x + (e.widget.winfo_x() if e.widget != self.win else 0)) / 10)
#         column = lambda e: int((e.y + (e.widget.winfo_y() if e.widget != self.win else 0)) / 10)
#         self.win.bind('<Button-3>', lambda e: print(f'row {row(e)}, column {column(e)}'))

# class Card:
#     _cAcHe = [] # because tkinter's garbage collector destroys self.image in __init__
#     def __init__(self, master, card_value = None, shirt_up: bool = False) -> None:
#         if not card_value:
#             pass #TODO:
#         else:
#             self.rank = card_value[0]
#             self.suit = card_value[1]
#         self.master = master
#         self.shirt_up = shirt_up
#         if self.shirt_up:
#             pass #TODO:
#         else:
#             self.file = DIR + r'\gfx\cards\\' + str(DECK.index(card_value)) + '.png'
#         self.image = tk.PhotoImage(master=self.master, file=self.file).subsample(1)
#         self.__class__._cAcHe += [self.image]
#         self.label = tk.Label(master, image=self.image)


#     def grid(self, row: int, column: int) -> None:
#         self.label.grid(row=row, column=column, rowspan=13, columnspan=8, sticky='NWES')

#     @classmethod
#     def clear_cAcHeD(cls):
#         cls._cAcHe = []


# CODE_NAME_EXISTS = GameCode(732, NameExistsError)
# CODE_SUCCESS = GameCode(700)
# CODE_SHUT_CONN = GameCode(710, GameClosedError)


# # First window - main menu
# start_menu = Window('menu', TITLE, bg=Params.color_BG)
# icon_pic = tk.PhotoImage(master=start_menu.win, file=DIR+'/gfx/logo.png')
# start_menu.win.iconphoto(True, icon_pic)

# start_menu.enable_debug()

# # Adding the stuff that will be always visible
# label_00_heading = tk.Label(start_menu.win, text='Card Games Catalogue'.upper(), font=Params.font_head, fg='yellow', bg=Params.color_BG)
# label_00_heading.grid(row=1, column=1, rowspan=4, columnspan=48, sticky='WE')

# # Sheet 0 - start menu
# button_00_menu_host_game = tk.Button(start_menu.win, cnf_menu_button, text='Host game',
#     command=lambda: game_parameters.update({'Server' : 'Server'}) or initial_nickname(lambda: start_menu.show(1)))
# button_00_menu_join_game = tk.Button(start_menu.win, cnf_menu_button, text='Join game',
#     command=lambda: game_parameters.update({'Server' : 'Client'}) or initial_nickname(lambda: action_join_game()))
# button_00_nickname = tk.Button(start_menu.win, cnf_menu_button, text='Change name',
#     command=lambda: change_nickname(lambda: start_menu.show(0)))
# button_00_quit = tk.Button(start_menu.win, cnf_menu_button, text='Quit',
#     command=start_menu.win.quit)

# button_00_menu_host_game.grid(cnf_lbl_g, row=10, column=13, columnspan=24)
# button_00_menu_join_game.grid(cnf_lbl_g, row=15, column=13, columnspan=24)
# button_00_nickname.grid(cnf_lbl_g, row=20, column=13, columnspan=24)
# button_00_quit.grid(cnf_lbl_g, row=25, column=13, columnspan=24)

# start_menu.add_sheet(0, button_00_menu_host_game, button_00_menu_join_game, button_00_quit, button_00_nickname)

# # Sheet 1 - game choose
# button_01_back = tk.Button(start_menu.win, cnf_menu_button, text='Back', command=lambda: start_menu.show(max(start_menu.current_sheet - 1, 0)))
# button_01_poker = tk.Button(start_menu.win, cnf_menu_button, text='Poker', command=lambda: action_host('Poker'))
# button_01_durak = tk.Button(start_menu.win, cnf_menu_button, text='Durak', command=lambda: action_host('Durak'))

# button_01_poker.grid(row=10, column=18, rowspan=4, columnspan=14, sticky='NESW')
# button_01_durak.grid(row=15, column=18, rowspan=4, columnspan=14, sticky='NESW')
# button_01_back.grid(cnf_lbl_g, row=25, column=18, columnspan=14)

# start_menu.add_sheet(1, button_01_poker, button_01_durak, button_01_back)

# # Sheet 2 - lobby (server)
# label_02_lobby = tk.Label(start_menu.win, text='LOBBY', font=Params.font_head, fg='yellow', bg=Params.color_BG)
# label_02_players = tk.Label(start_menu.win, cnf_lbl, text='Players:', font=Params.font_head, anchor='w')

# button_02_start = tk.Button(start_menu.win, cnf_menu_button, text='Start')
# button_02_close = tk.Button(start_menu.win, cnf_menu_button, text='Close')
# button_02_bool_omaha = tk.Button(start_menu.win, fg='black', bg='#e33', activebackground='#ee3')
# text_02_omaha = tk.Label(start_menu.win, cnf_lbl, text='Omaha version', font=Params.FONT_MIDDLE)
# button_02_bool_omaha.configure(command=lambda: button_02_bool_omaha.configure(bg=['#e33', '#3e3'][game_parameters['Variation'] == 'Poker']))

# text_02_server = tk.Label(start_menu.win, cnf_lbl,
#     text=f'Your IP-address is {get_ip()}\n* Tell Your friends to connect to this IP-address\n* Make sure the {PORT} port is open',
#     font=Params.FONT_MIDDLE, justify='left', wraplength=480, anchor='w', padx=2)
# img = tk.PhotoImage(master=start_menu.win, file = DIR + r'/gfx/copy.png')
# button_02_copy = tk.Button(start_menu.win, image=img, command=lambda: start_menu.win.clipboard_clear() or start_menu.win.clipboard_append(get_ip))
# button_02_copy.tkraise(text_02_server)

# def _1(i):
#     temp = tk.Label(start_menu.win, bg=['#3ed647', '#3eba47'][i % 2], anchor='w', font=Params.font_head, relief='raised', padx=7)
#     temp.grid(cnf_lbl_g, row=13+4*i, column=1, columnspan=24)
#     return temp

# lst_02_players = [_1(i) for i in range(8)]

# button_02_bool_omaha.grid(cnf_lbl_g, row=46, column=1, columnspan=4)
# text_02_omaha.grid(cnf_lbl_g, row=46, column=5, columnspan=20)
# text_02_server.grid(row=51, column=1, rowspan=9, columnspan=48, sticky='NEWS')
# label_02_lobby.grid(row=5, column=1, rowspan=4, columnspan=48, sticky='WE')
# label_02_players.grid(cnf_lbl_g, row=9, column=1, columnspan=18)
# button_02_copy.grid(row=52, column=44, rowspan=2, columnspan=2, sticky='NEWS')
# button_02_start.grid(cnf_lbl_g, row=13, column=38, columnspan=10)
# button_02_close.grid(cnf_lbl_g, row=18, column=38, columnspan=10)

# start_menu.add_sheet(2, button_02_bool_omaha, button_02_close,
#     text_02_omaha, text_02_server, label_02_lobby, button_02_start,
#     button_02_copy, label_02_players, lst_02_players)

# # Sheet 3 - lobby (player)
# button_03_leave = tk.Button(start_menu.win, cnf_menu_button, text='Leave')
# button_03_leave.grid(cnf_lbl_g, row=13, column=38, columnspan=10)

# start_menu.add_sheet(3, lst_02_players, button_03_leave, label_02_lobby, label_02_players)

# # Second window - player nickname choose
# middle_screen = Window('middle', TITLE, start_menu, Params.color_BG)

# # Adding the stuff that will be always visible
# label_1_msg = tk.Label(middle_screen.win, bg=Params.color_BG, fg=Params.color_warning, font=Params.font_head)
# button_1_back_to_menu = tk.Button(middle_screen.win, cnf_menu_button, text='Back')

# button_1_back_to_menu.grid(cnf_lbl_g, row=2, column=40, columnspan=8)
# label_1_msg.grid(cnf_lbl_g, row=7, column=2, columnspan=46)

# # 0 sheet - client
# label_10_address = tk.Label(middle_screen.win, cnf_lbl, text='IP-Address', font=Params.FONT_MIDDLE)
# entry_10_ip_address = tk.Entry(middle_screen.win, font=Params.FONT_MIDDLE, bg='CadetBlue1')
# button_10_join = tk.Button(middle_screen.win, cnf_menu_button, text='Join')

# label_10_address.grid(cnf_lbl_g, row=2, column=2, columnspan=11)
# entry_10_ip_address.grid(cnf_lbl_g, row=2, column=14, columnspan=16)
# button_10_join.grid(cnf_lbl_g, row=2, column=31, columnspan=8)

# middle_screen.add_sheet(0, entry_10_ip_address, label_10_address, button_10_join)

# # 1 sheet - nickname choose
# entry_11_nickname = tk.Entry(middle_screen.win, font=Params.FONT_MIDDLE, bg='CadetBlue1')
# label_11_nickname = tk.Label(middle_screen.win, cnf_lbl, text='Nickname', font=Params.FONT_MIDDLE)
# button_11_save = tk.Button(middle_screen.win, cnf_menu_button, text='Save')

# entry_11_nickname.grid(cnf_lbl_g, row=2, column=14, columnspan=16)
# label_11_nickname.grid(cnf_lbl_g, row=2, column=2, columnspan=11)
# button_11_save.grid(cnf_lbl_g, row=2, column=31, columnspan=8)

# middle_screen.add_sheet(1, entry_11_nickname, label_11_nickname, button_11_save)

# # Third window - games itself
# game_screen = Window('game', TITLE, start_menu, Params.color_dark_blue) # 100x80

# # Always visible widgets
# label_2_bg = tk.Label(game_screen.win, bg=Params.color_BG)
# label_2_bg.grid(row=0, column=0, rowspan=80, columnspan=90, sticky='NSEW')

# aboba = font.Font(family='Sylfaen', name='appHighlightFont', size=12, weight='bold')
# print(*font.families(), sep='\n')

# # Poker table
# _label_20_table_img = tk.PhotoImage(master=game_screen.win, file= DIR + r'\gfx\table.png')
# label_20_table = tk.Label(game_screen.win, text='table', image=_label_20_table_img) #bg=Params.color_white)
# label_20_players = tk.Label(game_screen.win, text='Players', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
# lst_20_players_nicknames = [tk.Label(game_screen.win, text='12345678901234', font=aboba, anchor='w',
#     bg=Params.color_dark_blue, fg=Params.color_gold) for i in range(8)]
# _lst_20_players_icons_imgs = [tk.PhotoImage(master=game_screen.win, file=DIR + f'\gfx\icons\icon{n % 3}.png') for n in range(8)]
# lst_20_players_icons = [tk.Label(game_screen.win, image=_lst_20_players_icons_imgs[i]) for i in range(8)]
# [lst_20_players_icons[i].grid(cnf_lbl_g, row=5 + 5*i, columnspan=5, column=90) for i in range(8)]
# [lst_20_players_nicknames[i].grid(cnf_lbl_g, row=5 + 5*i, column=95, columnspan=20) for i in range(8)]

# [Card(game_screen.win, (5+i, poker_util.DIAMOND)).grid(row=25, column=20+9*i) for i in range(5)]

# label_20_players.grid(cnf_lbl_g, row=0, column=90, columnspan=30)

# label_20_table.grid(row=12, column=4, rowspan=39, columnspan=76, sticky='NSEW')


# game_screen.add_sheet(0, label_20_table, label_20_players)


# # [Card(game_screen.win, DECK[i]).grid(row=1 + 14*(i // 11), column=1 + 9*(i % 11)) for i in range(52)]
# # Card(game_screen.win, DECK[2]).grid(1, 1, 13, 8)



# game_screen.enable_debug()



# # Deeds
# def change_nickname(func):
#     middle_screen.show(1)
#     start_menu.hide()
#     entry_11_nickname.delete(0, tk.END)
#     entry_11_nickname.insert(0, player_parameters['Name'])
#     def __(leave=False):
#         if not entry_11_nickname.get() and not leave:
#             label_1_msg['text'] = 'Enter a valid nickname'
#             middle_screen.win.after(3000, lambda: label_1_msg.configure(text=''))
#             return
#         middle_screen.hide()
#         if leave:
#             start_menu.show(0)
#         else:
#             player_parameters['Name'] = entry_11_nickname.get()
#             func()
#     button_11_save.configure(command=__)
#     button_1_back_to_menu.configure(command=lambda: __(True))

# def initial_nickname(func):
#     change_nickname(func) if not player_parameters['Name'] else func()

# def action_host(game):
#     game_parameters['Game'] = game
#     start_menu.show(2)
#     sock = socket.socket()
#     sock.bind(('', PORT))
#     sock.listen(10)

#     client_connections: dict[socket.socket, str] = {sock : player_parameters['Name']}
#     readers, listeners = [sock], []
#     trigger_is_closed, trigger_is_started = BoolTrigger(), BoolTrigger()

#     button_02_close.configure(command=trigger_is_closed.toggle)
#     button_02_start.configure(command=trigger_is_started.toggle)

#     lst_to_read: list[socket.socket]
#     lst_to_send: list[socket.socket]
#     while not (trigger_is_closed or trigger_is_started):
#         lst_to_read, lst_to_send, lst_faults = select.select(readers, listeners, [], 0.01)
#         for conn in lst_to_read:
#             if conn == sock:
#                 player, addr = sock.accept()
#                 player.setblocking(0)
#                 print(f'* Recieved connection (address {addr[0]}:{addr[1]})')
#                 readers += [player]
#             else:
#                 try:
#                     player_name = recvobj(conn)
#                     if not len(player_name):
#                         continue
#                     elif player_name in client_connections.values():
#                         sendobj(conn, CODE_NAME_EXISTS)
#                         conn.close()
#                     else:
#                         sendobj(conn, CODE_SUCCESS)
#                         client_connections[conn] = player_name
#                         listeners += [conn]
#                     readers.remove(conn)
#                 except ConnectionResetError:
#                     print(f'* Connection lost from player {conn.getpeername()}')
#                     client_connections.pop(conn)
#                     readers.remove(conn)
#                     listeners.remove(conn)

#         names = [*enumerate(client_connections.values())]
#         names = names + [(i, '') for i in range(8) if i not in [*zip(*names)][0]]
#         for conn in lst_to_send:
#             if conn in client_connections:
#                 try:
#                     sendobj(conn, names)
#                 except ConnectionError:
#                     print(f'* Player {client_connections[conn]} disconnected')
#                     listeners.remove(conn)
#                     client_connections.pop(conn)
#                     conn.close()
#         [lst_02_players[item[0]].configure(text=item[1]) for item in names]
#         middle_screen.win.update()

#     if trigger_is_closed:
#         for conn in client_connections:
#             if conn == sock:
#                 continue
#             sendobj(conn, CODE_SHUT_CONN)
#             conn.close()
#         sock.close()
#         middle_screen.hide()
#         start_menu.show(1)
#     else:
#         print('aboba')
#         pass #TODO: proceed into game
#         '''
#         * Create Players from cc list
#         * Shuffle Players list (prolly move to the PokerTable game method)
#         * Start the game
#         '''

#     return

# def message(msg: str):
#     label_1_msg['text'] = msg
#     middle_screen.win.after(3000, lambda: label_1_msg.configure(text='none'))

# def action_join_game():
#     def connection_attempt():
#         ip = entry_10_ip_address.get()
#         p_name = player_parameters['Name']
#         def _():
#             button_10_join.configure(state='disabled')
#             sock = socket.socket()
#             sock.settimeout(3)
#             try:
#                 sock.connect((ip, PORT))
#                 sendobj(sock, p_name)
#                 answer: GameCode = recvobj(sock)
#                 if answer.is_ok:
#                     return sock
#                 else:
#                     sock.close()
#                     return answer.exception
#             except Exception as e:
#                 return e
#         if not check_ip_mask(ip):
#             message('Enter a valid IP-address')
#             return

#         sock = _()
#         button_10_join.configure(state='normal')
#         if isinstance(sock, Exception):
#             if sock in [NameExistsError, GameClosedError]:
#                 message(sock.args[0])
#             elif sock == TimeoutError:
#                 message('Connection timeout')
#             elif sock == ConnectionRefusedError:
#                 message('Couldn\'t connect to the host')
#             return

#         middle_screen.hide()
#         start_menu.show(3)
#         trigger_game_started, trigger_left_lobby = BoolTrigger(), BoolTrigger()
#         while not (trigger_game_started or trigger_left_lobby):
#             msg: Union[list[tuple[int, str]], GameCode] = recvobj(sock)
#             if not isinstance(msg, GameCode):
#                 [lst_02_players[item[0]].configure(text=item[1]) for item in msg]
#             elif msg == CODE_SHUT_CONN:
#                 trigger_left_lobby.toggle()
#             else:
#                 trigger_game_started.toggle()
#             start_menu.win.update()
#         if trigger_left_lobby:
#             sock.close()
#             message('Connection closed by host')
#             start_menu.hide()
#             middle_screen.show(0)
#             return
#         pass # TODO: start the game

#     start_menu.hide()
#     middle_screen.show(0)

#     button_10_join.configure(command=lambda: threading.Thread(target=connection_attempt).start())

#     pass

# # start_menu.show(0)

# game_screen.show(0)

# start_menu.mainloop()
import tkinter as tk


root = tk.Tk()
bu = tk.Button(root, text='aboba', command=lambda: bu.place_configure())
bu.place(x=-(30 + 100), y=60, width=100, relx=1)

bu2 = tk.Button(root, text='2', command=lambda: bu.place())
bu2.place(x=10, y=20, width=100, height=40)


root.mainloop()