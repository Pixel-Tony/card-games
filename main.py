from src.util import *
import threading as thr
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

label_20_table = tk.Label(win_game.win, image=WImage(win_game, DIR + r'\gfx\misc\table.png'))
label_20_players = tk.Label(win_game.win, text='Players', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
label_20_line = tk.Label(win_game.win, bg=Params.color_white)
label_20_chat = tk.Label(win_game.win, text='Chat', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
canvas_20_chat = tk.Canvas(win_game.win, bg=Params.color_black, highlightcolor=Params.color_gold)
entry_20_chatmsg = smartify_entry(tk.Entry(win_game.win, bg=Params.color_grey, fg=Params.color_black, font=Params.font_super_low)) #TODO: params
button_20_send = tk.Button(win_game.win) #TODO: image

button_20_send.grid(CNF_LABEL_G, row=84, column=134, columnspan=4)
entry_20_chatmsg.grid(CNF_LABEL_G, row=84, column=112, columnspan=21)
canvas_20_chat.grid(CNF_IMAGE_G, row=53, column=112, rowspan=30, columnspan=26)

lst_20_players_nicknames = [
    tk.Label(win_game.win, text='', font=Params.font_players, anchor='w',
    bg=Params.color_dark_blue, fg=Params.color_gold) for i in range(8)]


button_20_check = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Check')
button_20_call = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Call')
button_20_show = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Show')

button_20_bet = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Bet')
button_20_raise = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Raise')

button_20_fold = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Fold')
button_20_muck = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Muck')

button_20_quit = tk.Button(win_game.win, CNF_MENU_BUTTON, text='Quit')

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


################################################################# Deeds
_message_id = None

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

    button_11_back.configure(
        command=Window.quit_window
        if initial else
        lambda: switch_windows(win_middle, win_menu, sheet_main_menu))

    switch_windows(win_menu, win_middle, sheet_nickname)

def initial_nickname_check():
    if player_parameters['Name'] == '':
        change_nickname(True)

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
                player, address = sock.accept()
                if len(connections) == 8:
                    sendobj(player, CODE_SERVER_FULL)
                    player.close()
                    continue
                player.setblocking(0)
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

    if t_is_closed:                                       # "Close" button pressed
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

    if t_left_lobby:                                      # disconnected
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



def poker_session(sock: socket.socket, *, connections: dict[socket.socket, str] = ..., this_p_name: str = ...):
    def print_message(name: str, args: tuple):
        if name == None: # message by system
            chat.add_line(args)
            pass
        else:
            chat.add_line('{GREEN}' + name + '{}: ' + args)
            pass

        pass#DO increase chat size if needed


    def send_msg(player=False, *, queue: MyPrimitiveEventQueue = None):
        def _player():
            sendobj(sock, MyEvent(10, this_p_name, text))

        def _server():
            queue.push(MyEvent(10, this_p_name, text))

        text = entry_20_chatmsg.get()
        entry_20_chatmsg.delete(0, tk.END)

        thr.Thread(target=[_server, _player][player]).start()

    def show_table_cards(cards: list[Card]):
        pass

    def disconnect_player(name: str, args: tuple):
        if name == this_p_name:                                 #TODO means player sent an ask for disconnection and server approved
            pass
        pass

    def player_action(name: str, args: tuple):
        if name == this_p_name:
            pass
        pass

    chat = CanvasChat((8, 8), canvas_20_chat, Params.font_super_low, Params.color_gold, 260)

    player_actions = {
        -1      : disconnect_player,
        0       : print_message,
        **{i    : player_action for i in range(1, 9)},
        10      : print_message
    }

    def _player(sock: socket.socket, this_p_name: str):
        button_20_send.configure(command=lambda: send_msg(True))
        names_with_positions: list[tuple[int, str]] = recvobj(sock)

        # dummy players for GUI interactions
        players = [PokerPlayer(name, i, 'dummy', win_game) for i, name in names_with_positions]

        [lst_20_players_nicknames[i].configure(text=f'-> {player}')
        or lst_20_players_nicknames[i].grid(CNF_LABEL_G, row=5*(i + 1), column=112, columnspan=20)
        for i, player in names_with_positions]

        switch_windows(win_menu, win_game, sheet_poker)

        t_finished, t_quit = Trigger(), Trigger()
        while not (t_finished or t_quit or Window.quit):
            t.sleep(0.001)
            data: MyEvent = recvobj(sock)
            if isinstance(data, MyEvent):
                player_actions[data.code](data.name, data.args)

            elif isinstance(data, GameCode):                    # codes support
                pass

            elif isinstance(data, socket.socket):               # game broke, disconnect
                pass

            pass

            win_game.win.update()

        if Window.quit:
            return

        if t_quit:
            switch_windows(win_game, win_menu, sheet_main_menu)
            return

        pass




    # [Card(win_game, (ORDER[8 + i], DIAMOND), small=True).grid(row=33, column=33 + 9*i) for i in range(5)]

    def _server(sock: socket.socket, connections: dict[socket.socket, str], this_p_name: str):
        button_20_send.configure(command=lambda: send_msg(queue=event_queue))
        event_queue = MyPrimitiveEventQueue()

        connections_lst, player_lst = [list(a) for a in zip(*connections.items())]
        shuffle(player_lst)
        player_lst = [*enumerate(player_lst)]

        for conn in connections:
            if conn == sock:
                continue
            sendobj(conn, player_lst)

        [lst_20_players_nicknames[i].configure(text=f'-> {player}')
            or lst_20_players_nicknames[i].grid(CNF_LABEL_G, row=5*(i + 1), column=112, columnspan=20)
            for i, player in player_lst]

        switch_windows(win_menu, win_game, sheet_poker)

        t_host_quit, t_game_finished = Trigger(), Trigger()
        pass #TODO: triggers?

        while not(t_host_quit or t_game_finished):
            t.sleep(0.016)
            lst_to_read, *dump = select.select(connections_lst, connections_lst, connections_lst, 0.001)
            for conn in lst_to_read:
                if conn == sock:
                    continue                                    # skip incoming connection attempts
                data = recvobj(conn)
                if not data:
                    continue
                elif isinstance(data, MyEvent):
                    event_queue.push(data)
                elif isinstance(data, GameCode):                # for codes receivement support
                    pass
                elif isinstance(data, socket.socket):           # socket broke, disconnect player after buffering "quit" action for him
                    pass

            event = event_queue.pop()
            # TODO: divide by tags:
            # chat - chat messages, send to everyone
            # game - PokerTable takes them, don't take them here



            for conn in connections:
                if conn == sock and event:
                    player_actions[event.code](event.name, event.args)
                else:
                    sendobj(conn, event)


            pass

            win_game.win.update()




    _player(sock, this_p_name) if connections == ... else _server(sock, connections, this_p_name)





# win_menu.show(sheet_main_menu)
# initial_nickname_check()

win_game.show(sheet_poker)

win_menu.mainloop()
