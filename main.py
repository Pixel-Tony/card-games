from core import *

player_stats = PlayerData.load()
print('Getting IP Address...')
IP, PORT = Network.ip_get(), 50240
print('IP and Port found;')
# menu Window
win_menu = GUIWindow((500, 600), TITLE, bg=Colors.BG)
_win_icon = tk.PhotoImage(master=win_menu.win, file='./gfx/misc/logo.png')
win_menu.win.iconphoto(True, _win_icon)

label_00_heading = tk.Label(win_menu.win,
                            text='TONY\'S CARD GAMES',
                            font=Fonts.HEAD,
                            fg='yellow',
                            bg=Colors.BG
                            )

label_00_heading.place(x=10, y=10, width=480, height=40)

# 1 layer - menu
button_00_menu_host_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Host game', command=lambda: win_menu.show(layer_0_game_choice))
button_00_menu_join_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Join game', command=lambda: game_join())
button_00_nickname = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Change name', command=lambda: nickname_change())
button_00_quit = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Quit', command=lambda: destruction_routine())

button_00_menu_host_game.place(CNF_MENU_BUTTON_P, y=100)
button_00_menu_join_game.place(CNF_MENU_BUTTON_P, y=150)
button_00_nickname.place(CNF_MENU_BUTTON_P, y=200)
button_00_quit.place(CNF_MENU_BUTTON_P, y=250)

layer_0_main_menu = GUIWindowLayer(win_menu, [button_00_menu_host_game,
    button_00_menu_join_game, button_00_nickname, button_00_quit]
)

# 2 layer - for game choice
button_01_poker = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Poker', command=lambda: game_host('Poker'))
button_01_durak = tk.Button(win_menu.win, CNF_MENU_BUTTON, state='disabled',
    text='Durak', command=lambda: game_host('Durak'))
button_01_back = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Back', command=lambda: win_menu.show(layer_0_main_menu))

button_01_poker.place(CNF_GAME_CHOICE_BUTTON_P, y=100)
button_01_durak.place(CNF_GAME_CHOICE_BUTTON_P, y=150)
button_01_back.place(CNF_GAME_CHOICE_BUTTON_P, y=250)

layer_0_game_choice = GUIWindowLayer(win_menu,
    [button_01_poker, button_01_durak, button_01_back])

# 3 layer - lobby itself
label_02_lobby = tk.Label(win_menu.win,
    text='LOBBY', fg='yellow', font=Fonts.HEAD, bg=Colors.BG
)
label_02_players = tk.Label(win_menu.win, CNF_LABEL,
    text='Players:', font=Fonts.HEAD, anchor='w'
)

button_02_start = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Start')
button_02_close = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Close')
button_02_omaha = tk.Button(win_menu.win,
    fg='black', bg='#e33', activebackground='#ee3',
    command=lambda: button_02_omaha.configure(
        bg=['#e33', '#3e3'][button_02_omaha['bg'] == '#e33']
    )
)

label_02_omaha = tk.Label(win_menu.win, CNF_LABEL,
    text='Omaha', font=Fonts.MIDDLE)
label_02_server = tk.Label(win_menu.win, CNF_LABEL,
    text=f'Your IP-address is {IP}', font=Fonts.MIDDLE, anchor='w')
button_02_copy = tk.Button(
    win_menu.win,
    image=Sprite(win_menu, './gfx/misc/copy.png'),
    command=lambda: win_menu.win.clipboard_clear()
        or win_menu.win.clipboard_append(IP)
)

def lobby_name_labels():
    out: list[tk.Label] = []
    for i in range(8):
        temp = tk.Label(win_menu.win, bg=['#4e4', '#3b4'][i % 2],
            anchor='w', font=Fonts.HEAD, relief='raised', padx=7
        )
        temp.place(height=40, width=240, x=10, y=130 + 40*i)
        out += [temp]
    return out

lst_02_players = lobby_name_labels()

label_02_omaha.place(height=40, width=200, x=50, y=460)
label_02_server.place(height=40, width=310, x=10, y=510)
label_02_lobby.place(height=40, width=480, x=10, y=50)
label_02_players.place(height=40, width=180, x=10, y=90)
button_02_copy.place(height=20, width=20, x=320, y=520)
button_02_omaha.place(height=40, width=40, x=10, y=460)
button_02_start.place(height=40, width=100, x=380, y=130)
button_02_close.place(height=40, width=100, x=380, y=130)

layer_0_lobby_host = GUIWindowLayer(win_menu,
    [label_02_lobby, label_02_players, *lst_02_players,
    button_02_start, button_02_close, label_02_omaha,
    button_02_omaha, label_02_server, button_02_copy]
)

button_03_leave = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Leave')
button_03_leave.place(width=100, height=40, x=380, y=130)

layer_0_lobby_player = GUIWindowLayer(win_menu,
    [*lst_02_players, button_03_leave, label_02_lobby, label_02_players]
)

# menu Middle
win_middle = GUIWindow((500, 130), TITLE, Colors.BG)

label_1_message = tk.Label(
    win_middle.win, bg=Colors.BG, fg=Colors.WARNING, font=Fonts.HEAD
)
label_1_message.place(width=460, height=40, x=20, y=70)

# 1 layer - pre-connection
label_10_address = tk.Label(win_middle.win, CNF_LABEL,
    text='IP-Address', font=Fonts.MIDDLE
)
entry_10_ip_address = GUIModernEntry(win_middle.win, CNF_ENTRY)
button_10_join = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Join')
button_10_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

label_10_address.place(width=110, height=40, x=20, y=20)
entry_10_ip_address.place(width=160, height=40, x=140, y=20)
button_10_join.place(width=80, height=40, x=310, y=20)
button_10_back.place(width=80, height=40, x=400, y=20)

layer_1_connection = GUIWindowLayer(win_middle,
    [entry_10_ip_address, button_10_back, label_10_address, button_10_join]
)

# 2 layer - nickname change
entry_11_nickname = GUIModernEntry(win_middle.win, CNF_ENTRY)
label_11_nickname = tk.Label(win_middle.win, CNF_LABEL,
    text='Nickname', font=Fonts.MIDDLE
)
button_11_save = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Save')
button_11_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

entry_11_nickname.place(width=160, height=40, x=140, y=20)
label_11_nickname.place(width=110, height=40, x=20, y=20)
button_11_save.place(width=80, height=40, x=310, y=20)
button_11_back.place(width=80, height=40, x=400, y=20)

layer_1_nickname = GUIWindowLayer(win_middle,
    [entry_11_nickname, label_11_nickname, button_11_save, button_11_back]
)

# window Game
win_game = GUIWindow((1400, 900), TITLE, Colors.DBLUE)
# background
tk.Label(
    win_game.win, bg=Colors.BG_GAME
).place(width=1100, height=900, x=0, y=0)

label_20_table = tk.Label(win_game.win,
    image=Sprite(win_game, './gfx/table.png')
)
label_20_players = tk.Label(win_game.win,
    text='Players', bg=Colors.DBLUE, font=Fonts.HEAD, fg=Colors.WHITE
)
label_20_chat = tk.Label(win_game.win,
    text='Chat', bg=Colors.DBLUE, font=Fonts.HEAD, fg=Colors.WHITE
)
label_20_line = tk.Label(win_game.win, bg=Colors.WHITE)
canvas_20_chat = tk.Canvas(win_game.win,
    bg=Colors.PITCH_BLACK, highlightcolor=Colors.GOLD,
    scrollregion=(0, 0, 230, 300)
)
scrollbar_20 = tk.Scrollbar(win_game.win,
    orient='vertical', command=canvas_20_chat.yview
)
canvas_20_chat.configure(width=230, height=300,
    yscrollcommand=scrollbar_20.set
)#TODO: check if can be config'd earlier

entry_20_chat = GUIModernEntry(win_game.win,
    bg=Colors.GREY, fg=Colors.PITCH_BLACK, font=Fonts.CHAT
)
button_20_msgsend = tk.Button(win_game.win,
    text='▶', font=('Helvetica', '30', 'bold'), foreground=Colors.DBLUE
)

lst_20_nicknames: list[tk.Label] = []
for _ in range(8):
    lst_20_nicknames.append(tk.Label(win_game.win,
        font=Fonts.PLAYER_TABLE, anchor='w', bg=Colors.DBLUE, fg=Colors.GOLD
    ))
    lst_20_nicknames[-1].place(width=300, height=40, x=1100, y=40 + 40*_)

button_20_check = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Check')
button_20_call = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Call')
button_20_show = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Show')

button_20_bet = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Bet')
button_20_raise = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Raise')

button_20_fold = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Fold')
button_20_muck = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Muck')

# To leave the current game, but remain in the lobby as a viewer
button_20_quit = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Quit')
# To disconnect from the lobby
button_20_leave = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Leave game')

slider_20_betting = tk.Scale #TODO

#TODO
# # # #
for button in [button_20_check, button_20_call, button_20_show]:
    button.place
for button in [button_20_bet, button_20_raise]:
    button.place
for button in [button_20_fold, button_20_muck]:
    button.place
button_20_quit.place
slider_20_betting.place
# # # #
#

label_20_players. place(width=300, height=40,  x=1100, y=0)
label_20_line.    place(width=256, height=2,   x=1122, y=468)
label_20_chat.    place(width=300, height=40,  x=1100, y=480)
label_20_table.   place(width=860, height=390, x=120,  y=200)
button_20_msgsend.place(width=40,  height=40,  x=1340, y=840)
entry_20_chat.    place(width=210, height=40,  x=1120, y=840)
canvas_20_chat.   place(width=230, height=300, x=1120, y=530)
scrollbar_20.     place(width=30,  height=300, x=1350, y=530)

layer_2_poker = GUIWindowLayer(win_game, [
    label_20_table,
    label_20_players,
    label_20_chat,
    label_20_line,
    canvas_20_chat,
    scrollbar_20,
    entry_20_chat,
    *lst_20_nicknames,
    # slider_20_betting,
    button_20_msgsend,
    button_20_check,
    button_20_call,
    button_20_show,
    button_20_bet,
    button_20_raise,
    button_20_fold,
    button_20_muck,
    button_20_quit,
    button_20_leave,
])

def game_host(*args): ...
def game_join(*args): ...
def nickname_change(): ...

def destruction_routine():
    PlayerData.write()
    GUIWindow.destroy()

def debug_game():
    for lbl in lst_20_nicknames:
        lbl.configure(text='Test')
    win_game.show(layer_2_poker, True)
    win_game.mainloop()

def debug_middle():
    win_middle.show(layer_1_connection, True)
    win_middle.mainloop()

if __name__ == '__main__':
    win_middle.hide()
    win_game.hide()
    win_menu.hide()
    #debug_middle()
    debug_game()
    # win_menu.show(layer_0_main_menu, True)
    # win_menu.mainloop()
