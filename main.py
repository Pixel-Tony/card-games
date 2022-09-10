from core import *

player_stats = PlayerData.load()
print('Getting IP Address...')
IP, PORT = Network.ip_get(), 50240
print('IP and Port found;')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Main graphical part
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Window for main menu
win_menu = GUIWindow((500, 600), TITLE, bg=Colors.BG)
_win_icon = tk.PhotoImage(master=win_menu.win, file='./gfx/misc/logo.png')
win_menu.win.iconphoto(True, _win_icon)

label_00_heading = tk.Label(
    win_menu.win, text='TONY\'S CARD GAMES',
    font=Fonts.HEAD, fg='yellow', bg=Colors.BG)

label_00_heading.place(x=10, y=10, width=480, height=40)

# 1 layer - menu
button_00_menu_host_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Host game', command=lambda: win_menu.show(layer_0_game_choice))
button_00_menu_join_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Join game', command=lambda: on_connmenu_enter())
button_00_nickname = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Change name', command=lambda: nickname_change())
button_00_quit = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Quit', command=lambda: on_quit())

button_00_menu_host_game.place(width=240, height=40, x=130, y=100)
button_00_menu_join_game.place(width=240, height=40, x=130, y=150)
button_00_nickname.      place(width=240, height=40, x=130, y=200)
button_00_quit.          place(width=240, height=40, x=130, y=250)

layer_0_main_menu = GUIWindowLayer(
    win_menu,
    [button_00_menu_host_game, button_00_menu_join_game,
        button_00_nickname, button_00_quit]
)

# 2 layer - for game choice
button_01_poker = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Poker', command=lambda: on_lobby_create('Poker'))
button_01_durak = tk.Button(win_menu.win, CNF_MENU_BUTTON, state='disabled',
    text='Durak', command=lambda: on_lobby_create('Durak'))
button_01_back = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Back', command=lambda: win_menu.show(layer_0_main_menu))

button_01_poker.place(height=40, width=140, x=180, y=100)
button_01_durak.place(height=40, width=140, x=180, y=150)
button_01_back. place(height=40, width=140, x=180, y=250)

layer_0_game_choice = GUIWindowLayer(win_menu,
    [button_01_poker, button_01_durak, button_01_back])

# 3 layer - lobby itself
label_02_lobby = tk.Label(
    win_menu.win, text='LOBBY', fg='yellow', font=Fonts.HEAD, bg=Colors.BG)
label_02_players = tk.Label(
    win_menu.win, CNF_LABEL, text='Players:', font=Fonts.HEAD, anchor='w')
label_02_omaha = tk.Label(win_menu.win, CNF_LABEL,
    text='Omaha', font=Fonts.MIDDLE)
label_02_server = tk.Label(win_menu.win, CNF_LABEL,
    text=f'Your IP-address is {IP}', font=Fonts.MIDDLE, anchor='w')

button_02_start = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Start')
button_02_close = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Close')
button_02_omaha = tk.Button(
    win_menu.win, fg='black', activebackground='#ee3', bg='#e33',
    command=lambda: button_02_omaha.configure(
        bg=['#e33', '#3e3'][button_02_omaha['bg'] == '#e33']))
button_02_copy = tk.Button(
    win_menu.win,
    image=Sprite(win_menu, './gfx/misc/copy.png'),
    command=lambda: [win_menu.win.clipboard_clear(),
        win_menu.win.clipboard_append(IP)]
)

def _0():
    out: list[tk.Label] = []
    for i in range(8):
        temp = tk.Label(win_menu.win, bg=['#4e4', '#3b4'][i % 2],
            anchor='w', font=Fonts.HEAD, relief='raised', padx=7
        )
        temp.place(height=40, width=240, x=10, y=130 + 40*i)
        out += [temp]
    return out
lst_02_players = _0()

label_02_omaha.  place(width=200, height=40, x=50,  y=460)
label_02_server. place(width=310, height=40, x=10,  y=510)
label_02_lobby.  place(width=480, height=40, x=10,  y=50)
label_02_players.place(width=180, height=40, x=10,  y=90)
button_02_copy.  place(width=20,  height=20, x=320, y=520)
button_02_omaha. place(width=40,  height=40, x=10,  y=460)
button_02_start. place(width=100, height=40, x=380, y=130)
button_02_close. place(width=100, height=40, x=380, y=130)

layer_0_lobby_host = GUIWindowLayer(
    win_menu,
    [
        label_02_lobby, label_02_players, *lst_02_players, button_02_start,
        button_02_close, label_02_omaha, button_02_omaha, label_02_server,
        button_02_copy
    ]
)

# 4 layer - lobby view for simple player
button_03_leave = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Leave')
button_03_leave.place(width=100, height=40, x=380, y=130)

layer_0_lobby_player = GUIWindowLayer(
    win_menu,
    [*lst_02_players, button_03_leave, label_02_lobby, label_02_players])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Window for middle menu
win_middle = GUIWindow((500, 130), TITLE, Colors.BG)

label_1_message = tk.Label(
    win_middle.win, bg=Colors.BG, fg=Colors.WARNING, font=Fonts.HEAD)
label_1_message.place(width=460, height=40, x=20, y=70)

# 1 layer - pre-connection
label_10_address = tk.Label(
    win_middle.win, CNF_LABEL, text='IP-Address', font=Fonts.MIDDLE)
entry_10_ip_address = GUIModernEntry(win_middle.win, CNF_ENTRY)
button_10_join = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Join')
button_10_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

label_10_address.place(width=110, height=40, x=20, y=20)
entry_10_ip_address.place(width=160, height=40, x=140, y=20)
button_10_join.place(width=80, height=40, x=310, y=20)
button_10_back.place(width=80, height=40, x=400, y=20)

layer_1_connection = GUIWindowLayer(
    win_middle,
    [entry_10_ip_address, button_10_back, label_10_address, button_10_join])

# 2 layer - nickname change
entry_11_nickname = GUIModernEntry(win_middle.win, CNF_ENTRY)
label_11_nickname = tk.Label(
    win_middle.win, CNF_LABEL, text='Nickname', font=Fonts.MIDDLE)
button_11_save = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Save')
button_11_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

entry_11_nickname.place(width=160, height=40, x=140, y=20)
label_11_nickname.place(width=110, height=40, x=20,  y=20)
button_11_save.   place(width=80,  height=40, x=310, y=20)
button_11_back.   place(width=80,  height=40, x=400, y=20)

layer_1_nickname = GUIWindowLayer(
    win_middle,
    [entry_11_nickname, label_11_nickname, button_11_save, button_11_back])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Window for game
win_game = GUIWindow((1400, 900), TITLE, Colors.DBLUE)

# background
tk.Label(win_game.win, bg=Colors.BG_GAME).place(width=1100, height=900)

label_20_table = tk.Label(
    win_game.win, image=Sprite(win_game, './gfx/table.png'))
label_20_players = tk.Label(
    win_game.win,
    text='Players', bg=Colors.DBLUE, font=Fonts.HEAD, fg=Colors.WHITE)
label_20_chat = tk.Label(
    win_game.win,
    text='Chat', bg=Colors.DBLUE, font=Fonts.HEAD, fg=Colors.WHITE)
label_20_line = tk.Label(win_game.win, bg=Colors.WHITE)
canvas_20_chat = tk.Canvas(
    win_game.win, bg=Colors.PITCH_BLACK,
    highlightcolor=Colors.GOLD, scrollregion=(0, 0, 230, 300),
    yscrollcommand=lambda f, l: scrollbar_20.set(f, l))
scrollbar_20 = tk.Scrollbar(
    win_game.win,
    orient='vertical', command=canvas_20_chat.yview)

entry_20_chat = GUIModernEntry(
    win_game.win, bg=Colors.GREY, fg=Colors.PITCH_BLACK, font=Fonts.CHAT)
button_20_msgsend = tk.Button(
    win_game.win, text='▶', font=('Helvetica', '30', 'bold'),
    foreground=Colors.DBLUE)

def _1(i):
    label = tk.Label(
        win_game.win, font=Fonts.PLAYER_TABLE,
        anchor='w', bg=Colors.DBLUE, fg=Colors.GOLD)
    label.place(width=300, height=40, x=1120, y=50 * (i + 1))
    return label

lst_20_nicknames: list[tk.Label] = [_1(i) for i in range(8)]

button_20_check = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Check')
button_20_call = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Call')
button_20_show = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Show')

button_20_bet = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Bet')
button_20_raise = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Raise')

button_20_fold = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Fold')
button_20_muck = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Muck')

button_20_quit = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Quit')
'Button for leaving the current game, but remain in the lobby as a viewer'

button_20_leave = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Leave game')
'Button for disconnecting from the lobby'

slider_20_betting = tk.Scale(win_game.win, command=print) #TODO command

#TODO positioning
# # # #
[button.place
    for button in [button_20_check, button_20_call, button_20_show]]
[button.place
    for button in [button_20_bet, button_20_raise]]
[button.place
    for button in [button_20_fold, button_20_muck]]
button_20_quit.place
slider_20_betting.place(width=80, height=200, x=100, y=100)
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
    slider_20_betting,
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Functionality ahead
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def on_lobby_create(game_type: str):
    win_menu.show(layer_0_lobby_host)

    tr_cancelled, tr_started = Trigger(), Trigger()
    button_02_close.configure(command=tr_cancelled.toggle)
    button_02_start.configure(command=tr_started.toggle)

    PokerServer(PORT).start(tr_started, tr_cancelled)

    while not (tr_cancelled or tr_started or GUIWindow.did_quit):
        win_menu.update()



def on_lobby_create_OLD(game: str):
    def on_player_disconnect(conn: Socket, left: bool = False): ...
    def on_lobby_cancel():
        for conn in connections:
            if conn is sock: continue
            Network.send(conn, GC_ERR_LOBBY_CLOSING)
            conn.close()
        sock.close()
        GUIWindow.switch_to(win_menu, layer_0_main_menu)

    button_02_start.configure(state='disabled')
    win_menu.show(layer_0_lobby_host)

    tr_cancelled, tr_started = Trigger(), Trigger()
    button_02_close.configure(command=tr_cancelled.toggle)
    button_02_start.configure(command=tr_started.toggle)

    sock = Socket()
    sock.bind(('', PORT))
    sock.listen(9)

    connections = {sock: {'Name' : PlayerData()['Name'], 'ID' : 'host'}}
    readers, listeners = [sock], []
    n_conns_pending = 0

    @wait_until_dt(1/50)
    def update():
        nonlocal n_conns_pending
        win_menu.update()

        lst_read, lst_send, _ = sel.select(readers, listeners, [], 0.001)
        for conn in lst_read:
            if conn == sock: # new connection
                player, address = sock.accept()
                if len(connections) == 9:
                    Network.send(player, GC_ERR_LOBBY_FULL)
                    player.close()
                    continue
                player.settimeout(3)
                connections[player] = {'Name': 'connecting...',
                                       'ID': "{}:{}".format(*address),
                                       'Pending' : True}
                readers.append(player)
                n_conns_pending += 1
                continue

            if (data := Network.receive(conn)) is None:
                continue
            elif isinstance(data, dict):
                event = data['Event']
                if (event == 'Leaves' or not Network.send(conn, GC_SUCCESS)):
                    on_player_disconnect(conn, event == 'Leaves')
                    continue
                connections[conn]['Name'] = data['Name']
                connections[conn]['Pending']
                n_conns_pending -= 1
            else:
                on_player_disconnect(conn)
        lst_names = [a['Name'] for a in connections.values()]
        lst_names += [''] * 7
        for conn in lst_send:
            if not Network.send(conn, lst_names):
                on_player_disconnect(conn)
        try:
            [lst_02_players[i].config(text=lst_names[i]) for i in range(8)]
            button_02_start['state'] = (
                B_STATES[n_conns_pending * (len(lst_names) - 1)])
        except tk.TclError:
            return on_lobby_cancel()

    while not any((tr_cancelled, tr_started, GUIWindow.did_quit)):
        update()


    #TODO
    on_lobby_cancel()

def on_connmenu_enter():
    def conn_attempt(): ...

    button_10_join.configure(command=conn_attempt)
    button_10_back.configure(command=lambda: GUIWindow.switch_to(
        win_menu, layer_0_main_menu))

    GUIWindow.switch_to(win_middle, layer_1_connection)

    while GUIWindow.current == win_middle:
        win_middle.update()

def nickname_change(initial: bool = False):
    def on_keypress(ev):
        win_middle.update()
        button_11_save.configure(
            state='normal' if entry_11_nickname.get() else 'disabled')

    def on_save_attempt():
        PlayerData()['Name'] = entry_11_nickname.get()
        win_middle.win.unbind_all('<Key>')
        GUIWindow.switch_to(win_menu, layer_0_main_menu)

    win_middle.win.bind('<Key>', on_keypress)
    entry_11_nickname.delete(0, tk.END)
    entry_11_nickname.insert(0, PlayerData()['Name'])

    button_11_save.configure(command=on_save_attempt,
        state=['normal', 'disabled'][initial])
    button_11_back.configure(
        command=on_quit
            if initial
                else lambda: GUIWindow.switch_to(win_menu, layer_0_main_menu)
    )
    GUIWindow.switch_to(win_middle, layer_1_nickname)

def initial_nickname_check():
    if PlayerData()['Name'] == '':
        nickname_change(True)

def on_quit():
    PlayerData.write()
    GUIWindow.destroy()

def debug_game():
    for lbl in lst_20_nicknames:
        lbl.configure(text='Test')
    win_game.show(layer_2_poker, True)
    win_game.mainloop()

if __name__ == '__main__':
    win_middle.hide()
    win_game.hide()
    win_menu.hide()
    # debug_game()
    win_menu.show(layer_0_main_menu, True)
    initial_nickname_check()
    win_menu.mainloop()
