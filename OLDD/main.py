from server import *
from poker import *

import threading as thr
import select

player_parameters = general_get_player_info()

##### First window - main menu
win_menu = Window((500, 600), TITLE, bg=Params.color_BG)
icon_pic = tk.PhotoImage(master=win_menu.win, file='./gfx/misc/logo.png')
win_menu.win.iconphoto(True, icon_pic)

win_menu.x_enable_debug()

    # Adding the stuff that will be always visible
label_00_heading = tk.Label(
    win_menu.win, text='Card Games Catalogue'.upper(),
    font=Params.font_head, fg='yellow', bg=Params.color_BG)
label_00_heading.grid(row=1, column=1, rowspan=4, columnspan=48, sticky='WE')

    # Sheet 0 - main menu
button_00_menu_host_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Host game', command=lambda: win_menu.show(sheet_game_choice))
button_00_menu_join_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Join game', command=lambda: game_join())
button_00_nickname = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Change name', command=lambda: change_nickname())
button_00_quit = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Quit', command=win_menu.win.quit)

button_00_menu_host_game.grid(CNF_LABEL_G, row=10, column=13, columnspan=24)
button_00_menu_join_game.grid(CNF_LABEL_G, row=15, column=13, columnspan=24)
button_00_nickname.grid(CNF_LABEL_G, row=20, column=13, columnspan=24)
button_00_quit.grid(CNF_LABEL_G, row=25, column=13, columnspan=24)

sheet_main_menu = WindowSheet(win_menu,
    grid_items=[button_00_menu_host_game, button_00_quit,
        button_00_menu_join_game, button_00_nickname])

    # Sheet 1 - game choose
button_01_poker = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Poker', command=lambda: game_host('Poker'))
button_01_durak = tk.Button(win_menu.win, CNF_MENU_BUTTON, state='disabled',
    text='Durak', command=lambda: game_host('Durak'))
button_01_back = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Back', command=lambda: win_menu.show(sheet_main_menu))

button_01_poker.grid(CNF_LABEL_G, row=10, column=18, columnspan=14)
button_01_durak.grid(CNF_LABEL_G, row=15, column=18, columnspan=14)
button_01_back.grid(CNF_LABEL_G, row=25, column=18, columnspan=14)

sheet_game_choice = WindowSheet(win_menu,
    grid_items=[button_01_poker, button_01_durak, button_01_back])

    # Sheet 2 - lobby (host)
label_02_lobby = tk.Label(
    win_menu.win, text='LOBBY', fg='yellow',
    font=Params.font_head, bg=Params.color_BG)
label_02_players = tk.Label(
    win_menu.win, CNF_LABEL, text='Players:',
    font=Params.font_head, anchor='w')

button_02_start = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Start')
button_02_close = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Close')
button_02_omaha = tk.Button(
    win_menu.win, fg='black', bg='#e33', activebackground='#ee3',
    command=lambda:
        button_02_omaha.configure(
            bg=['#e33', '#3e3'][button_02_omaha['bg'] == '#e33']))

text_02_omaha = tk.Label(win_menu.win, CNF_LABEL,
    text='Omaha version', font=Params.font_middle)
text_02_server = tk.Label(win_menu.win, CNF_LABEL,
    text=f'Your IP-address is {IP}', font=Params.font_middle, anchor='w')
button_02_copy = tk.Button(
    win_menu.win,
    image = Sprite(win_menu, './gfx/misc/copy.png'),
    command=lambda: win_menu.win.clipboard_clear()
        or win_menu.win.clipboard_append(IP))

def _names(i):
    temp = tk.Label(win_menu.win, bg=['#3ed647', '#3cba45'][i % 2],
        anchor='w', font=Params.font_head, relief='raised', padx=7)
    temp.grid(CNF_LABEL_G, row=13 + 4*i, column=1, columnspan=24)
    return temp

lst_02_players = [_names(i) for i in range(8)]

text_02_omaha.grid(CNF_LABEL_G, row=46, column=5, columnspan=20)
text_02_server.grid(CNF_LABEL_G, row=51, column=1, columnspan=31)
label_02_lobby.grid(row=5, column=1, rowspan=4, columnspan=48, sticky='WE')
label_02_players.grid(CNF_LABEL_G, row=9, column=1, columnspan=18)
button_02_copy.grid(CNF_IMG_G, row=52, column=32, rowspan=2, columnspan=2)
button_02_omaha.grid(CNF_LABEL_G, row=46, column=1, columnspan=4)
button_02_start.grid(CNF_LABEL_G, row=13, column=38, columnspan=10)
button_02_close.grid(CNF_LABEL_G, row=18, column=38, columnspan=10)

sheet_lobby_host = WindowSheet(win_menu,
    grid_items=[
        label_02_lobby, label_02_players, *lst_02_players,
        button_02_start, button_02_close, text_02_omaha,
        button_02_omaha, text_02_server, button_02_copy
    ])

    # Sheet 3 - lobby (player)
button_03_leave = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Leave')
button_03_leave.grid(CNF_LABEL_G, row=13, column=38, columnspan=10)

sheet_lobby_player = WindowSheet(win_menu,
    grid_items=[*lst_02_players, button_03_leave,
                label_02_lobby, label_02_players])

##### Second window - player nickname choose
win_middle = Window((500, 130), TITLE, win_menu, Params.color_BG)

    # Adding the stuff that will be always visible
label_1_message = tk.Label(win_middle.win, bg=Params.color_BG,
    fg=Params.color_warning, font=Params.font_head)

label_1_message.grid(CNF_LABEL_G, row=7, column=2, columnspan=46)

    # 0 sheet - client
label_10_address = tk.Label(win_middle.win, CNF_LABEL,
    text='IP-Address', font=Params.font_middle)
entry_10_ip_address = entry_smartify(tk.Entry(win_middle.win,
    font=Params.font_middle, bg='CadetBlue1'))
button_10_join = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Join')
button_10_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

label_10_address.grid(CNF_LABEL_G, row=2, column=2, columnspan=11)
entry_10_ip_address.grid(CNF_LABEL_G, row=2, column=14, columnspan=16)
button_10_join.grid(CNF_LABEL_G, row=2, column=31, columnspan=8)
button_10_back.grid(CNF_LABEL_G, row=2, column=40, columnspan=8)

sheet_connect = WindowSheet(win_middle,
    grid_items=[
        entry_10_ip_address, button_10_back,
        label_10_address, button_10_join
    ])

    # 1 sheet - nickname choose
entry_11_nickname = entry_smartify(tk.Entry(win_middle.win,
    font=Params.font_middle, bg='CadetBlue1'))
label_11_nickname = tk.Label(win_middle.win, CNF_LABEL,
    text='Nickname', font=Params.font_middle)
button_11_save = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Save')
button_11_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

entry_11_nickname.grid(CNF_LABEL_G, row=2, column=14, columnspan=16)
label_11_nickname.grid(CNF_LABEL_G, row=2, column=2, columnspan=11)
button_11_save.grid(CNF_LABEL_G, row=2, column=31, columnspan=8)
button_11_back.grid(CNF_LABEL_G, row=2, column=40, columnspan=8)

sheet_nickname = WindowSheet(win_middle,
    grid_items=[
        entry_11_nickname, label_11_nickname,
        button_11_save, button_11_back
    ])

##### Third window - game itself; 1400x900 = 140 x 90
win_game = Window((1400, 900), TITLE, win_menu, Params.color_dark_blue)

    # Always visible widgets - background
tk.Label(
    win_game.win, bg=Params.color_BG_game
    ).grid(row=0, column=0, rowspan=90, columnspan=110, sticky='NSEW')

    # Sheet 0 - Poker table
sheet_poker = WindowSheet(win_game)

label_20_table = tk.Label(win_game.win,
    image=Sprite(win_game, './gfx/table.png'))
label_20_players = tk.Label(win_game.win, text='Players',
    bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
label_20_chat = tk.Label(win_game.win, text='Chat',
    bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
label_20_line = tk.Label(win_game.win, bg=Params.color_white)

canvas_20_chat = tk.Canvas(win_game.win, bg=Params.color_black,
    highlightcolor=Params.color_gold, scrollregion=(0, 0, 230, 300))
scrollbar_20 = tk.Scrollbar(win_game.win, orient='vertical',
    command=canvas_20_chat.yview)
canvas_20_chat.configure(width=230, height=300,
    yscrollcommand=scrollbar_20.set)

entry_20_chatmsg = entry_smartify(tk.Entry(win_game.win,
    #TODO: params
    bg=Params.color_grey, fg=Params.color_black, font=Params.font_chat))
button_20_send = tk.Button(win_game.win, text='▶',
    font=('Helvetica', '30', 'bold'), foreground=Params.color_dark_blue)

button_20_send.grid(CNF_LABEL_G, row=84, column=134, columnspan=4)
entry_20_chatmsg.grid(CNF_LABEL_G, row=84, column=112, columnspan=21)
canvas_20_chat.grid(CNF_IMG_G, row=53, column=112, rowspan=30, columnspan=23)
scrollbar_20.grid(CNF_IMG_G, row=53, column=135, rowspan=30, columnspan=3)

lst_20_players_nicknames = [
    tk.Label(win_game.win, text='', font=Params.font_players, anchor='w',
    bg=Params.color_dark_blue, fg=Params.color_gold) for i in range(8)]

button_20_check = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_CHECK)
button_20_call = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_CALL)
button_20_show = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_SHOW)

button_20_bet = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_BET)
button_20_raise = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_RAISE)

button_20_fold = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_FOLD)
button_20_muck = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_MUCK)

button_20_quit = tk.Button(win_game.win, CNF_MENU_BUTTON, text=ACTIONS_QUIT)

button_20_disconnect: tk.Button = None #TODO:

slider_20_bet: tk.Scale = None #TODO: slider for betting and raising

for button in [button_20_check, button_20_call, button_20_show]:
    button.grid(CNF_GAME_BUTTON_G) #DO
    sheet_poker.add_grid(button)

for button in [button_20_bet, button_20_raise]:
    button.grid(CNF_GAME_BUTTON_G) #DO
    sheet_poker.add_grid(button)

for button in [button_20_fold, button_20_muck]:
    button.grid(CNF_GAME_BUTTON_G) #DO
    sheet_poker.add_grid(button)

button_20_quit.grid(CNF_GAME_BUTTON_G) #DO
sheet_poker.add_grid(button_20_quit)

label_20_table.grid(CNF_IMG_G, row=20, column=12, rowspan=39, columnspan=86)
label_20_players.grid(CNF_LABEL_G, row=0, column=110, columnspan=30)
label_20_line.place(x=1122, y=468, width=256, height=2)
label_20_chat.grid(CNF_LABEL_G, row=48, column=110, columnspan=30)

sheet_poker.add_grid(label_20_table, label_20_players, label_20_chat)
sheet_poker.add_place(label_20_line)

win_game.x_enable_debug()

_message_id = None

############################################################################
#                    Functions and methods for the game                    #
############################################################################
def message(msg: str):
    global _message_id
    if label_1_message['text'] != '':
        win_middle.win.after_cancel(_message_id)

    label_1_message['text'] = msg
    _message_id = win_middle.win.after(4500,
        lambda: label_1_message.configure(text=''))

def error_message(code: GameCodeType):
    return {
        GCODE_SHUT_CONNECTION : 'Connection closed by host',
        GCODE_SERVER_FULL : 'Lobby is full',
    }[code]

def change_nickname(initial: bool = False):
    def control_button_state(ev: tk.Event):
        win_middle.update()
        button_11_save.configure(
            state='normal'
                if entry_11_nickname.get()
                    else 'disabled')

    def confirm_attempt():
        msg = entry_11_nickname.get()
        if not msg:
            message('Enter a valid nickname')
            return

        player_parameters['name'] = msg
        win_middle.win.unbind_all('<Key>')
        Window.switch(win_middle, win_menu, sheet_main_menu)

    win_middle.win.bind('<Key>', control_button_state)
    entry_11_nickname.delete(0, tk.END)
    entry_11_nickname.insert(0, player_parameters['name'])

    button_11_save.configure(command=confirm_attempt,
        state=['normal', 'disabled'][initial])
    button_11_back.configure(command=Window.main_quit
        if initial
            else lambda:
                Window.switch(win_middle, win_menu, sheet_main_menu))

    Window.switch(win_menu, win_middle, sheet_nickname)

def initial_nickname_check():
    if player_parameters['name'] == '':
        change_nickname(True)

# # # # # # # # # # # # # # | Game host function | # # # # # # # # # # # # #
def game_host(game: Literal['Poker', 'Durak']):
    def disconnect_player(conn: Socket, left: bool = False):
        if left:
            sendobj(conn, GCODE_DISCONNECT)
        if conn in readers:
            readers.remove(conn)
        if conn in listeners:
            listeners.remove(conn)
        if conn in connections:
            connections.pop(conn)
        conn.close()

    def close_lobby():
        for conn in connections:
            if conn == sock:
                continue
            sendobj(conn, GCODE_SHUT_CONNECTION)
            conn.close()
        sock.close()
        Window.switch(win_middle, win_menu, sheet_main_menu)

    if game != 'Poker':
        button_02_omaha.grid_remove()

    button_02_start.configure(state='disabled')
    win_menu.show(sheet_lobby_host)

    t_is_closed, t_is_started = Trigger(), Trigger()
    button_02_close.configure(command=t_is_closed.toggle)
    button_02_start.configure(command=t_is_started.toggle)

    sock = Socket()
    sock.bind(('', PORT))
    sock.listen(10)

    connections: dict[Socket, dict[str, str]] = {}
    connections[sock] = {'name' : player_parameters['name'], 'id' : 'HOST'}

    readers, listeners = [sock], []
    lst_read: list[Socket]
    lst_send: list[Socket]

    # to prevent one in a thrillion chance of going into game
        # while someone haven't sent his name yet
    n_connecting = 0

    @delta_time(0.016)
    def update():
        nonlocal n_connecting
        win_menu.update()

        lst_read, lst_send = select.select(readers, listeners, [], 0.001)[:-1]
        for conn in lst_read:
            # new connection received
            if conn == sock:
                player, address = sock.accept()
                if len(connections) == 8:
                    sendobj(player, GCODE_SERVER_FULL)
                    player.close()
                    continue

                player.settimeout(SOCKET_TIMEOUT)
                connections[player] = {
                    'name' : 'connecting...',
                    'id' : ':'.join(map(str, address))
                }
                readers.append(player)
                n_connecting += 1
                continue

            data = recvobj(conn)

            if not data:
                continue
            # If recieved info is name and sent GCODE_SUCCESS is recieved
            # by the player:
            elif isinstance(data, str) and not sendobj(conn, GCODE_SUCCESS):
                connections[conn] = {
                    'name' : data,
                    'id' : (data, connections[conn]['id'])
                    }
                n_connecting -= 1
                listeners.append(conn)
                continue

            disconnect_player(conn, data == GCODE_DISCONNECT)

        names = [connections[a]['name'] for a in connections]

        for conn in lst_send:
            if sendobj(conn, names):
                disconnect_player(conn)

        try:
            [lst_02_players[i].configure(text=(names + ['']*7)[i])
                for i in range(8)]

            button_02_start.configure(
                state='disabled'
                    if (len(connections) < 2 or n_connecting)
                    else 'normal')
        except tk.TclError:
            # closed window while in lobby
            return

    while not (t_is_closed or t_is_started) and not Window.did_quit:
        update()

    # if quit app
    if Window.did_quit:
        return close_lobby()

    # if "Close" button pressed
    if t_is_closed:
        return close_lobby()

    # Game start
    for conn in connections:
        if conn == sock:
            continue

        if sendobj(conn, GCODE_SUCCESS):
            return close_lobby()

    result = poker_session(sock, connections)
    #TODO: handle result



# # # # # # # # # # # # # # | Game join function | # # # # # # # # # # # # #
def option_join():
    while game_join():
        continue

def game_join() -> bool:
    '''
    Literally handle whole game
    In only case which is "left the lobby" will return 1
    '''
    def conn_attempt(ip) -> Union[Socket, str]:
        nonlocal sock
        p_name = player_parameters['name']
        if not validate_ip(ip):
            message('Enter a valid IP')
            sock = 0
            return

        button_10_join.configure(state='disabled')
        button_10_back.configure(state='disabled')
        sock_attempt = Socket(socket_AF_INET, socket_SOCK_STREAM)
        sock_attempt.settimeout(SOCKET_TIMEOUT)

        try:
            sock_attempt.connect((ip, PORT))
            sendobj(sock_attempt, p_name)
            answer: GameCodeType = recvobj(sock_attempt)
            if answer != GCODE_SUCCESS:
                message(error_message(answer))
            else:
                sock = sock_attempt
        except TimeoutError:
            message('Connection attempt timed out')
        except ConnectionRefusedError:
            message('Couldn\'t connect')

        button_10_join.configure(state='normal')
        button_10_back.configure(state='normal')
        if sock == None:
            sock = 0

    def run_conn_attempt():
        ip = entry_10_ip_address.get()
        thread = thr.Thread(target=conn_attempt, args=(ip,))
        thread.start()

    button_10_join.configure(command=run_conn_attempt)

    button_10_back.configure(command=lambda:
        Window.switch(win_middle, win_menu, sheet_main_menu))
    button_03_leave.configure(command=lambda:
        Window.switch(win_menu, win_middle, sheet_connect))

    Window.switch(win_menu, win_middle, sheet_connect)

    while Window.current() == win_middle:
        sock: Socket = None

        while sock == None and Window.current() == win_middle:
            t.sleep(0.005)
            win_middle.update()
            if Window.did_quit:
                return 0

        # if left window
        if Window.current() != win_middle:
            # ...and if connected before he did
            if isinstance(sock, Socket):
                sendobj(sock, GCODE_DISCONNECT)
                recvobj(sock)
            return 0
        # bad connection attempt but still at this window, continue the loop
        if sock == 0:
            continue
        # on successful connection attempt, leave the cycle, continue further
        break

    Window.switch(win_middle, win_menu, sheet_lobby_player)
    t_game_started, t_left_lobby = Trigger(), Trigger()
    t_game_aborted = Trigger()
    t_gp = t_game_aborted, t_game_started, t_left_lobby

    @delta_time(0.016)
    def update():
        win_menu.update()

        data: Union[list[str], GameCodeType] = recvobj(sock)
        if isinstance(data, list):
            data += ['']*8
            try:
                for i in range(8):
                    lst_02_players[i].configure(text=data[i])
            except tk.TclError:
                return 0
        elif data == GCODE_SHUT_CONNECTION:
            t_left_lobby.toggle()
        elif data == GCODE_SUCCESS:
            t_game_started.toggle()
        else:
            t_game_aborted.toggle()
        return None

    while not (any(t_gp) or Window.current() != win_menu or Window.did_quit):
        if update() == 0:
            return 0

    if Window.did_quit:
        # quit game
        return 0

    if t_game_started:
        result = poker_session(sock)
        if result[0] == 0:
            return 0
        else:
            message(result)
        #TODO: handle result
        return 0

    elif t_left_lobby:
        Window.switch(win_menu, win_middle, sheet_connect)
        message('Game closed')

    elif Window.current() != win_menu:
        sendobj(sock, GCODE_DISCONNECT)
        recvobj(sock)

    # quit lobby
    return 1

# # # # # # # # # # # # # # | Poker game function | # # # # # # # # # # # # #
def poker_session(sock: Socket,
                  connections: dict[Socket, dict[str, str]] = ...
                  ) -> tuple[int, str]:
    '''
    Return value[0]:
    1 - failure (Connection lost), value[1] - error message
    0 - success
    '''
    IS_OMAHA = recvobj(sock)
    if isinstance(IS_OMAHA, Socket):
        return (1, 'Connection lost')

    CARDS_DECK = {
        card: {
            'small' : CardSprite(win_game, card, True),
            'normal': CardSprite(win_game, card, False),
        } for card in DECK
    }

    def GUI_show_table_cards(table_cards: list[CardValue]):
        '''Show table (preflop, flop, river) cards on the table'''
        [CARDS_DECK[card]['normal'].place(330, 330 + 90*i)
            for i, card in enumerate(table_cards)]

    def GUI_hide_table_cards(table_cards: list[CardValue]):
        [CARDS_DECK[card]['normal'].hide() for card in table_cards]

    def GUI_card_showdown(p: PlayerGUI, cards: list[CardValue]):
        p.real_cards_show(cards, IS_OMAHA)

    def action_react(ev: Event):
        pass

    def parse_event(ev: Event):
        pass

    def play_as_host() -> tuple[int, str]:
        pass

    def play_as_server() -> tuple[int, str]:
        pass

    return [play_as_host, play_as_server][connections != ...]()

# # # # # # # # # # # # # # # | Main function | # # # # # # # # # # # # # # #
def main():
    win_menu.show(sheet_main_menu)
    initial_nickname_check()
    win_menu.mainloop_start()

def debug():
    ps = [PlayerGUI(win_game, i, 'abobus') for i in range(8)]
    CARDS_DECK = {
        card: {
            'small' : CardSprite(win_game, card, True),
            'normal': CardSprite(win_game, card, False),
        } for card in DECK
    }
    win_game.show(sheet_poker)

    for p in ps:
        p.bind_card_sprite_pool(CARDS_DECK)
        p.table_cards_show()
        p.bankroll_update(1000)
        p.tokens_update()
        p.real_cards_show([(ORDER[j + ps.index(p)], SUITS[ps.index(p) % 4]) for j in range(2)], 1)

    win_game.x_enable_debug()
    win_game.win.bind("<Button-1>", lambda ev: ps[2].frame_highlight())
    win_game.win.bind("<Button-3>", lambda ev: ps[2].real_cards_show([DECK[0], DECK[17]]), '+')


    [CardSprite(win_game, ('J', SUITS[i % 4])).place(330 + 90*i, 330) for i in range(5)]
    win_game.mainloop_start()


if __name__ == "__main__":
    # debug()
    main()
