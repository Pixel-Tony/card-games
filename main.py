from src.util import *
import select

##### First window - main menu
win_menu = Window('menu', TITLE, bg=Params.color_BG)
icon_pic = tk.PhotoImage(master=win_menu.win, file=DIR+r'\gfx\misc\logo.png')
win_menu.win.iconphoto(True, icon_pic)

win_menu.enable_debug()

    # Adding the stuff that will be always visible
label_00_heading = tk.Label(win_menu.win, text='Card Games Catalogue'.upper(), font=Params.font_head, fg='yellow', bg=Params.color_BG)
label_00_heading.grid(row=1, column=1, rowspan=4, columnspan=48, sticky='WE')

    # Sheet 0 - main menu
button_00_menu_host_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Host game', command=lambda: win_menu.show(sheet_game_choice))
button_00_menu_join_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Join game', command=lambda: join_game())
button_00_nickname = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Change name', command=lambda: change_nickname())
button_00_quit = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Quit', command=win_menu.win.quit)

button_00_menu_host_game.grid(CNF_LABEL_G, row=10, column=13, columnspan=24)
button_00_menu_join_game.grid(CNF_LABEL_G, row=15, column=13, columnspan=24)
button_00_nickname.grid(CNF_LABEL_G, row=20, column=13, columnspan=24)
button_00_quit.grid(CNF_LABEL_G, row=25, column=13, columnspan=24)

sheet_main_menu = WindowSheet(win_menu,
    grid_items=[button_00_menu_host_game, button_00_menu_join_game, button_00_quit, button_00_nickname])

    # Sheet 1 - game choose
button_01_poker = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Poker', command=lambda: host_game('Poker'))
button_01_durak = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Durak', command=lambda: host_game('Durak'))
button_01_back = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Back', command=lambda: win_menu.show(sheet_main_menu))

button_01_poker.grid(CNF_LABEL_G, row=10, column=18, columnspan=14)
button_01_durak.grid(CNF_LABEL_G, row=15, column=18, columnspan=14)
button_01_back.grid(CNF_LABEL_G, row=25, column=18, columnspan=14)

sheet_game_choice = WindowSheet(win_menu,
    grid_items=[button_01_poker, button_01_durak, button_01_back])

    # Sheet 2 - lobby (host)
label_02_lobby = tk.Label(win_menu.win, text='LOBBY', font=Params.font_head, fg='yellow', bg=Params.color_BG)
label_02_players = tk.Label(win_menu.win, CNF_LABEL, text='Players:', font=Params.font_head, anchor='w')

button_02_start = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Start')
button_02_close = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Close')
button_02_omaha = tk.Button(win_menu.win, fg='black', bg='#e33', activebackground='#ee3',
    command=lambda: button_02_omaha.configure(bg=['#e33', '#3e3'][button_02_omaha['bg'] == '#e33'])) # why to change variables when you can change button colors

text_02_omaha = tk.Label(win_menu.win, CNF_LABEL, text='Omaha version', font=Params.font_middle)
text_02_server = tk.Label(win_menu.win, CNF_LABEL, text=f'Your IP-address is {IP}', font=Params.font_middle, anchor='w')
button_02_copy = tk.Button(win_menu.win, image = WImage(win_menu, DIR + r'\gfx/misc/copy.png'),
    command=lambda: win_menu.win.clipboard_clear() or win_menu.win.clipboard_append(IP))

def _names(i):
    temp = tk.Label(win_menu.win, bg=['#3ed647', '#3cba45'][i % 2], anchor='w', font=Params.font_head, relief='raised', padx=7)
    temp.grid(CNF_LABEL_G, row=13 + 4*i, column=1, columnspan=24)
    return temp

lst_02_players = [_names(i) for i in range(8)]

text_02_omaha.grid(CNF_LABEL_G, row=46, column=5, columnspan=20)
text_02_server.grid(CNF_LABEL_G, row=51, column=1, columnspan=31)
label_02_lobby.grid(row=5, column=1, rowspan=4, columnspan=48, sticky='WE')
label_02_players.grid(CNF_LABEL_G, row=9, column=1, columnspan=18)
button_02_copy.grid(CNF_IMAGE_G, row=52, column=32, rowspan=2, columnspan=2)
button_02_omaha.grid(CNF_LABEL_G, row=46, column=1, columnspan=4)
button_02_start.grid(CNF_LABEL_G, row=13, column=38, columnspan=10)
button_02_close.grid(CNF_LABEL_G, row=18, column=38, columnspan=10)

sheet_lobby_host = WindowSheet(win_menu,
    grid_items=[label_02_lobby, label_02_players, lst_02_players,
    button_02_start, button_02_close, text_02_omaha,
    button_02_omaha, text_02_server, button_02_copy])

    # Sheet 3 - lobby (player)
button_03_leave = tk.Button(win_menu.win, CNF_MENU_BUTTON, text='Leave')
button_03_leave.grid(CNF_LABEL_G, row=13, column=38, columnspan=10)

sheet_lobby_player = WindowSheet(win_menu,
    grid_items=[lst_02_players, button_03_leave, label_02_lobby, label_02_players])

##### Second window - player nickname choose
win_middle = Window('middle', TITLE, win_menu, Params.color_BG)

    # Adding the stuff that will be always visible
label_1_message = tk.Label(win_middle.win, bg=Params.color_BG, fg=Params.color_warning, font=Params.font_head)
label_1_message.grid(CNF_LABEL_G, row=7, column=2, columnspan=46)

    # 0 sheet - client
label_10_address = tk.Label(win_middle.win, CNF_LABEL, text='IP-Address', font=Params.font_middle)
entry_10_ip_address = smartify_entry(tk.Entry(win_middle.win, font=Params.font_middle, bg='CadetBlue1'))
button_10_join = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Join')
button_10_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

label_10_address.grid(CNF_LABEL_G, row=2, column=2, columnspan=11)
entry_10_ip_address.grid(CNF_LABEL_G, row=2, column=14, columnspan=16)
button_10_join.grid(CNF_LABEL_G, row=2, column=31, columnspan=8)
button_10_back.grid(CNF_LABEL_G, row=2, column=40, columnspan=8)

sheet_connect = WindowSheet(win_middle,
    grid_items=[entry_10_ip_address, label_10_address, button_10_join, button_10_back])

    # 1 sheet - nickname choose
entry_11_nickname = smartify_entry(tk.Entry(win_middle.win, font=Params.font_middle, bg='CadetBlue1'))
label_11_nickname = tk.Label(win_middle.win, CNF_LABEL, text='Nickname', font=Params.font_middle)
button_11_save = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Save')
button_11_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

entry_11_nickname.grid(CNF_LABEL_G, row=2, column=14, columnspan=16)
label_11_nickname.grid(CNF_LABEL_G, row=2, column=2, columnspan=11)
button_11_save.grid(CNF_LABEL_G, row=2, column=31, columnspan=8)
button_11_back.grid(CNF_LABEL_G, row=2, column=40, columnspan=8)

sheet_nickname = WindowSheet(win_middle,
    grid_items=[entry_11_nickname, label_11_nickname, button_11_save, button_11_back])

##### Third window - game itself
win_game = Window('game', TITLE, win_menu, Params.color_dark_blue) # 1400x900 - 140 x 90

    # Always visible widgets
tk.Label(win_game.win, bg=Params.color_BG_game).grid(row=0, column=0, rowspan=90, columnspan=110, sticky='NSEW') # background

    # Sheet 0 - Poker table
sheet_poker = WindowSheet(win_game)

label_20_table = tk.Label(win_game.win, image=WImage(win_game, DIR + r'\gfx\misc\table3.png'))
label_20_players = tk.Label(win_game.win, text='Players', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
label_20_line = tk.Label(win_game.win, bg=Params.color_white)
label_20_chat = tk.Label(win_game.win, text='Chat', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)

canvas_20_chat = tk.Canvas(win_game.win, bg=Params.color_black, highlightcolor=Params.color_gold, scrollregion=(0, 0, 230, 300))
_scrollbar_20_chat = tk.Scrollbar(win_game.win, orient='vertical', command=canvas_20_chat.yview)
canvas_20_chat.configure(width=230, height=300, yscrollcommand=_scrollbar_20_chat.set)

entry_20_chatmsg = smartify_entry(tk.Entry(win_game.win, bg=Params.color_grey, fg=Params.color_black, font=Params.font_super_low)) #TODO: params
button_20_send = tk.Button(win_game.win) #TODO: image

button_20_send.grid(CNF_LABEL_G, row=84, column=134, columnspan=4)
entry_20_chatmsg.grid(CNF_LABEL_G, row=84, column=112, columnspan=21)
canvas_20_chat.grid(CNF_IMAGE_G, row=53, column=112, rowspan=30, columnspan=23)
_scrollbar_20_chat.grid(row=53, column=135, rowspan=30, columnspan=3, sticky='NEWS')

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

#TODO: seats

label_20_table.grid(CNF_IMAGE_G, row=20, column=12, rowspan=39, columnspan=86)
label_20_players.grid(CNF_LABEL_G, row=0, column=110, columnspan=30)
label_20_line.place(x=1122, y=468, width=256, height=2)
label_20_chat.grid(CNF_LABEL_G, row=48, column=110, columnspan=30)

sheet_poker.add_grid(label_20_table, label_20_players, label_20_chat)
sheet_poker.add_place(label_20_line)

win_game.enable_debug()


_message_id = None

################################################################# Facility
def message(msg: str):
    global _message_id
    if label_1_message['text'] != '':
        win_middle.win.after_cancel(_message_id)
    label_1_message['text'] = msg
    _message_id = win_middle.win.after(4500, lambda: label_1_message.configure(text=''))

def change_nickname(initial: bool = False):
    def button_control(ev):
        win_middle.win.update()
        button_11_save.configure(state='normal' if entry_11_nickname.get() else 'disabled')

    def confirm():
        if not entry_11_nickname.get():
            message('Enter a valid nickname')
            return
        player_parameters['Name'] = entry_11_nickname.get()
        win_middle.win.unbind_all('<Key>')
        switch_windows(win_middle, win_menu, sheet_main_menu)

    win_middle.win.bind('<Key>', button_control)
    entry_11_nickname.delete(0, tk.END)
    entry_11_nickname.insert(0, player_parameters['Name'])
    button_11_save.configure(command=confirm, state='disabled' if initial else 'normal')

    button_11_back.configure(command=
        Window.quit_window if initial else lambda: switch_windows(win_middle, win_menu, sheet_main_menu))

    switch_windows(win_menu, win_middle, sheet_nickname)

def initial_nickname_check():
    if player_parameters['Name'] == '':
        change_nickname(True)

################################################################# Connecting to and hosting games

def host_game(game: Literal['Poker', 'Durak']):
    def disconnect_player(conn: socket.socket, left: bool = False):
        if left:
            sendobj(conn, CODE_DISCONNECT)
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
            sendobj(conn, CODE_SHUT_CONN)
            conn.close()
        sock.close()
        switch_windows(win_middle, win_menu, sheet_main_menu)
    SocketList = list[socket.socket]

    game_parameters['Game'] = game
    if game != 'Poker':
        button_02_omaha.grid_remove()

    win_menu.show(sheet_lobby_host)

    t_is_closed, t_is_started = Trigger(), Trigger()
    button_02_close.configure(command=t_is_closed.toggle)
    button_02_start.configure(command=t_is_started.toggle)

    sock = socket.socket()
    sock.bind(('', PORT))
    sock.listen(10)

    connections: dict[socket.socket, str] = {sock : player_parameters['Name']}
    readers, listeners = [sock], []
    lst_to_read: SocketList
    lst_to_send: SocketList

    while not (t_is_closed or t_is_started) and not Window.quit:

        lst_to_read, lst_to_send, lst_faults = select.select(readers, listeners, [], 0.001) # ~ 60 fps lol
        t.sleep(0.016)
        for conn in lst_to_read:
            if conn == sock:                                    # new connection received
                player, address = sock.accept()                 # FUTURE name-independent player connection
                if len(connections) == 8:                           # by coding with address info
                    sendobj(player, CODE_SERVER_FULL)
                    player.close()
                    continue
                player.settimeout(SOCKET_TIMEOUT)
                readers.append(player)
                continue

            data = recvobj(conn)

            if not data:
                continue
            elif isinstance(data, str) and data not in connections.values():
                if not sendobj(conn, CODE_SUCCESS):             # == if successfully sent
                    connections[conn] = data
                    listeners.append(conn)
                    continue
            if data in connections.values():
                sendobj(conn, CODE_NAME_EXISTS)                 # disconnection reason

            disconnect_player(conn, data == CODE_DISCONNECT)

        for conn in lst_to_send:
            if conn == sock:
                continue
            if sendobj(conn, [*connections.values()]):
                disconnect_player(conn)

        for i in range(8):
            lst_02_players[i]['text'] = ([*connections.values()][i] if i < len(connections) else '')

        button_02_start.configure(state='disabled' if len(connections) < 2 else 'normal')
        win_menu.win.update()

    if Window.quit:                                             # if quit app
        return

    if t_is_closed:                                             # "Close" button pressed
        close_lobby()
        return

    # Game start, send CODE_SUCCESS to everybody,
    # then client_connections, then CODE_SUCCESS
    # again if everybody is still here
    for conn in connections:                                    # Game start
        if conn == sock:
            continue
        if sendobj(conn, CODE_SUCCESS):
            close_lobby()
            return
        sendobj(conn, [*connections.values()])
        sendobj(conn, CODE_SUCCESS)

    poker_session(sock, connections=connections, this_p_name=player_parameters['Name'])

def join_game():
    #NOTE You can't do stuff with widgets while in thread, so it's desirable that
        # all the parameters which depend on tk Window(s) will be given as arguments
    def connection_attempt(ip) -> Union[socket.socket, str]: # on "join" click
        nonlocal sock
        p_name = player_parameters['Name']
        if not check_ip_mask(ip):
            message('Enter a valid IP')
            sock = 0
            return

        button_10_join.configure(state='disabled')
        button_10_back.configure(state='disabled')              # you can't escape your destiny
        sock_attempt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_attempt.settimeout(SOCKET_TIMEOUT)

        try:
            sock_attempt.connect((ip, PORT))
            sendobj(sock_attempt, p_name)
            answer: GameCode = recvobj(sock_attempt)
            if answer != CODE_SUCCESS:
                message(answer.message)
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

    def run_thread():
        ip = entry_10_ip_address.get()
        thread = thr.Thread(target=connection_attempt, args=(ip,))
        thread.start()


    button_10_join.configure(command=run_thread)
    button_10_back.configure(command=lambda: switch_windows(win_middle, win_menu, sheet_main_menu))
    button_03_leave.configure(command=lambda: switch_windows(win_menu, win_middle, sheet_connect))

    switch_windows(win_menu, win_middle, sheet_connect)

    while Window.current_window == win_middle:
        sock: socket.socket = None

        while sock == None and Window.current_window == win_middle:
            t.sleep(0.005)
            win_middle.win.update()                             # event loop
            if Window.quit:                                     # quit app
                return

        if Window.current_window != win_middle:                 # if left window...
            if isinstance(sock, socket.socket):                 # ...and if connected before he did
                sendobj(sock, CODE_DISCONNECT)
                recvobj(sock)
            return                                              # left, so break the loop

        if sock == 0:                                           # bad connection attempt but still at window, continue the loop
            continue

        break                                                   # on successful connection attempt

    switch_windows(win_middle, win_menu, sheet_lobby_player)
    t_game_started, t_left_lobby = Trigger(), Trigger()

    while not (t_game_started or t_left_lobby) and Window.current_window == win_menu and not Window.quit:
        t.sleep(0.005)
        data: Union[list[str], GameCode] = recvobj(sock)
        if not isinstance(data, GameCode):
            client_connections = data
            [lst_02_players[i].configure(text = (client_connections + [''] * 8)[i]) for i in range(8)]
        elif data == CODE_SHUT_CONN:                            # host closed lobby
            t_left_lobby.toggle()
        elif data == CODE_SUCCESS:                              # game starts
            t_game_started.toggle()
        else:
            print(f'undescribed data received {data}')
        win_menu.win.update()

    if Window.quit:
        return

    if t_left_lobby:                                            # disconnected
        switch_windows(win_menu, win_middle, sheet_connect)
        message('Game closed')
        join_game()
        return

    if Window.current_window != win_menu:                       # left thru button
        sendobj(sock, CODE_DISCONNECT)
        recvobj(sock)
        join_game()
        return

    client_connections = recvobj(sock)

    # he fell off while continuing to the game
    # or somebody fell before and server shut
    if not client_connections or recvobj(sock) == CODE_SHUT_CONN:
        print('failure\a')
        switch_windows(win_menu, win_middle, sheet_connect)
        message('Connection lost' if not client_connections else 'Game closed')
        join_game()

    playing = True
    while playing:
        playing = poker_session(sock, this_p_name=player_parameters['Name'])
        pass
    pass
    #TODO: further depends on result

################################################################# Games sections
def poker_session(sock: socket.socket, *, connections: dict[socket.socket, str] = None, this_p_name: str = None):
    def print_message(name: str, args: str):
        '''print message to the game chat'''
        chat.add_line(args if name == None else f'#GREEN#{name}##: {args}')

    def move_to_queue(event: Event, *, sock: socket.socket = ...,
                      queue: EventQueue = None, tag = Q_ALL):
        sendobj(sock, event) if queue == None else queue.push(event, tag)

    def send_msg():
        def _target():
            move_to_queue(Event(10, this_p_name, text),
                sock=sock, queue=event_queue)                   # (queue == None) -> (== sendobj(...))

        button_20_send.configure(relief='raised')               # constant presses make it become sunken, why - nobody knows
        text = entry_20_chatmsg.get().strip()
        entry_20_chatmsg.delete(0, tk.END)

        if text != '':
            thr.Thread(target=_target).start()

    def show_table_cards():
        [card.grid(33, 33 + 9*i) for i, card in enumerate(table_cards)]

    def hide_table_cards():
        [card.hide() for card in table_cards]

    def disconnect(name: str, args):
        pass

    def continuation_choice(name: str, args):
        if connections == None:
            print_message(name, args)
            return
        pass


    def player_action(name: str, args: dict[Literal['txt', 'bet'], Union[str, int]]):
        def show_buttons(options: list[str]):
            '''options: list of ACTIONS_-constants'''
            for option in options:
                game_buttons_table[option].grid()

            for option in ACTIONS_CHECK, ACTIONS_BET, ACTIONS_FOLD:
                game_buttons_table[option]['state'] = 'normal'

        def hide_buttons():
            '''options: list of ACTIONS_-constants'''
            for option in _nonmain_options:
                game_buttons_table[option].grid_remove()

            for option in ACTIONS_CHECK, ACTIONS_BET, ACTIONS_FOLD:
                game_buttons_table[option]['state'] = 'disabled'

        if name != this_p_name:
            print_message(name)

        pass

    event_queue = EventQueue() if connections != None else None
    chat = CanvasChat((8, 8), canvas_20_chat, Params.font_super_low, Params.color_gold, 230)
    table_cards: list[Card] = []

    game_buttons_table = {
        ACTIONS_CHECK   : button_20_check,
        ACTIONS_CALL    : button_20_call,
        ACTIONS_SHOW    : button_20_show,

        ACTIONS_BET     : button_20_bet,
        ACTIONS_RAISE   : button_20_raise,

        ACTIONS_FOLD    : button_20_fold,
        ACTIONS_MUCK    : button_20_muck,

        ACTIONS_QUIT    : button_20_quit,
    }

    event_code_to_action_table = {                              # f(name: str, args: Any)
        -1              : disconnect,
        0               : print_message,
       **{i             : player_action for i in range(1, 9)},
        10              : print_message,
        11              : continuation_choice,
    }


    _nonmain_options = [ACTIONS_CALL, ACTIONS_MUCK,
        ACTIONS_QUIT, ACTIONS_RAISE, ACTIONS_SHOW]

    for option in game_buttons_table:
        if option in [ACTIONS_BET, ACTIONS_RAISE]:
            continue #TODO: bind these

        game_buttons_table[option].configure(command = lambda:
            move_to_queue(Event(Event.codes[option], this_p_name),
                sock=sock, queue=event_queue))

    button_20_send.configure(command=send_msg)

    def as_player():                                            # for the sake of different scopes
        names_with_positions: list[tuple[int, str]] = recvobj(sock)
        players: list[PokerPlayer] = []

        for i, player in names_with_positions:
            lst_20_players_nicknames[i].configure(text=f'-> {player}')
            lst_20_players_nicknames[i].grid(CNF_LABEL_G,
                row = 5*(i + 1), column=112, columnspan=20)

            players.append(PokerPlayer(player, i, 'dummy', win_game))

        switch_windows(win_menu, win_game, sheet_poker)

        t_finished, t_player_quit = Trigger(), Trigger()        # game finished; player chose to quit by himself
        t_aborted = Trigger()                                   # server closed

        while not (t_finished or t_player_quit or t_aborted or Window.quit):
            t.sleep(0.001)
            win_game.win.update()

            data: Union[Event, GameCode, socket.socket] = recvobj(sock)
            if not data:
                continue

            if isinstance(data, Event):
                if data.code == Event.codes['Shutdown']:
                    t_aborted.toggle()
                    break

                event_code_to_action_table[data.code](data.name, data.args)



                pass


            elif isinstance(data, GameCode):
                pass

            else:
                t_aborted.toggle()


        if Window.quit:
            return

        if t_player_quit:
            switch_windows(win_game, win_menu, sheet_main_menu)
            return

        if t_aborted:
            switch_windows(win_game, win_menu, sheet_main_menu)
            message('Game been aborted')
            join_game()
            return

        pass

    def as_host():
        connections_lst: list[socket.socket]
        player_lst: list[tuple[int, socket.socket]]

        connections_lst, player_lst = [list(a) for a in zip(*connections.items())]
        shuffle(player_lst)
        player_lst = [*enumerate(player_lst)]

        for conn in connections_lst:
            if conn == sock:
                continue
            sendobj(conn, player_lst)

        for i, player in player_lst:
            lst_20_players_nicknames[i].configure(text=f'-> {player}')
            lst_20_players_nicknames[i].grid(CNF_LABEL_G,
                row = 5*(i + 1), column=112, columnspan=20)

        switch_windows(win_menu, win_game, sheet_poker)

        game = PokerTable([PokerPlayer(connections[conn], i, conn) for i, conn in player_lst])
        thr.Thread(target=game.game, args=(button_02_omaha['bg'] == '#3e3',), daemon=True).start()


        t_game_finished = Trigger()
        while not (t_game_finished or Window.quit):
            t.sleep(0.016)
            win_game.win.update()

            lst_to_read, *dump = select.select(connections_lst, [], [], 0.001)
            for conn in lst_to_read:
                if conn == sock:
                    continue

                data = recvobj(conn)
                if not data:
                    continue
                if isinstance(data, Event):
                    event_queue.push(data)
                elif isinstance(data, GameCode):
                    pass
                elif isinstance(data, socket.socket):
                    pass

            event = event_queue.pop()
            # TODO: divide by tags:
            # chat - chat messages, send to everyone
            # game - PokerTable takes them, don't take them here
            # TODO: check if player which action is called is
            # still connected, otherwise add quit event to his buffer
            for conn in connections_lst:
                if conn == sock:
                    if event != None:
                        event_code_to_action_table[event.code](event.name, event.args)
                    pass
                    continue

                sendobj(conn, event)
                pass

            pass

        pass

    as_host() if connections != None else as_player()

################################################################# Start of the game

win_menu.show(sheet_main_menu)
initial_nickname_check()

# win_game.show(sheet_poker)

win_menu.mainloop()
