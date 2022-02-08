from src.util import *
import threading as thr
import select

##### First window - main menu
start_menu = Window('menu', TITLE, bg=Params.color_BG)
icon_pic = tk.PhotoImage(master=start_menu.win, file=DIR+r'\gfx\misc\logo.png')
start_menu.win.iconphoto(True, icon_pic)

start_menu.enable_debug()

    # Adding the stuff that will be always visible
label_00_heading = tk.Label(start_menu.win, text='Card Games Catalogue'.upper(), font=Params.font_head, fg='yellow', bg=Params.color_BG)
label_00_heading.grid(row=1, column=1, rowspan=4, columnspan=48, sticky='WE')

    # Sheet 0 - start menu
button_00_menu_host_game = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Host game', command=lambda: start_menu.show(1))
button_00_menu_join_game = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Join game', command=lambda: join_game())
button_00_nickname = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Change name', command=lambda: change_nickname())
button_00_quit = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Quit', command=start_menu.win.quit)

button_00_menu_host_game.grid(CNF_LABEL_G, row=10, column=13, columnspan=24)
button_00_menu_join_game.grid(CNF_LABEL_G, row=15, column=13, columnspan=24)
button_00_nickname.grid(CNF_LABEL_G, row=20, column=13, columnspan=24)
button_00_quit.grid(CNF_LABEL_G, row=25, column=13, columnspan=24)

start_menu.add_sheet(0, button_00_menu_host_game, button_00_menu_join_game, button_00_quit, button_00_nickname)

    # Sheet 1 - game choose
button_01_back = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Back', command=lambda: start_menu.show(0))
button_01_poker = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Poker', command=lambda: host_game('Poker'))
button_01_durak = tk.Button(start_menu.win, CNF_MENU_BUTTON,
    text='Durak', command=lambda: host_game('Durak'))

button_01_poker.grid(row=10, column=18, rowspan=4, columnspan=14, sticky='NESW')
button_01_durak.grid(row=15, column=18, rowspan=4, columnspan=14, sticky='NESW')
button_01_back.grid(CNF_LABEL_G, row=25, column=18, columnspan=14)

start_menu.add_sheet(1, button_01_poker, button_01_durak, button_01_back)

    # Sheet 2 - lobby (host)
label_02_lobby = tk.Label(start_menu.win, text='LOBBY', font=Params.font_head, fg='yellow', bg=Params.color_BG)
label_02_players = tk.Label(start_menu.win, CNF_LABEL, text='Players:', font=Params.font_head, anchor='w')

button_02_start = tk.Button(start_menu.win, CNF_MENU_BUTTON, text='Start')
button_02_close = tk.Button(start_menu.win, CNF_MENU_BUTTON, text='Close')
button_02_omaha = tk.Button(start_menu.win, fg='black', bg='#e33', activebackground='#ee3',
    command=lambda: button_02_omaha.configure(bg=['#e33', '#3e3'][button_02_omaha['bg'] == '#e33'])) # why to change variables when you can change colors

text_02_omaha = tk.Label(start_menu.win, CNF_LABEL, text='Omaha version', font=Params.font_middle)
text_02_server = tk.Label(start_menu.win, CNF_LABEL, text=f'Your IP-address is {IP}', font=Params.font_middle, anchor='w')
button_02_copy = tk.Button(start_menu.win, image = WImage(start_menu, DIR + r'\gfx/misc/copy.png'),
    command=lambda: start_menu.win.clipboard_clear() or start_menu.win.clipboard_append(IP))

def _names(i):
    temp = tk.Label(start_menu.win, bg=['#3ed647', '#3cba45'][i % 2], anchor='w', font=Params.font_head, relief='raised', padx=7)
    temp.grid(CNF_LABEL_G, row=13 + 4*i, column=1, columnspan=24)
    return temp

lst_02_players = [_names(i) for i in range(8)]

text_02_omaha.grid(CNF_LABEL_G, row=46, column=5, columnspan=20)
text_02_server.grid(row=51, column=1, rowspan=4, columnspan=31, sticky='NEWS')
label_02_lobby.grid(row=5, column=1, rowspan=4, columnspan=48, sticky='WE')
label_02_players.grid(CNF_LABEL_G, row=9, column=1, columnspan=18)
button_02_copy.grid(row=52, column=32, rowspan=2, columnspan=2, sticky='NEWS')
button_02_omaha.grid(CNF_LABEL_G, row=46, column=1, columnspan=4)
button_02_start.grid(CNF_LABEL_G, row=13, column=38, columnspan=10)
button_02_close.grid(CNF_LABEL_G, row=18, column=38, columnspan=10)

start_menu.add_sheet(2, button_02_omaha, button_02_close, text_02_omaha, text_02_server,
    label_02_lobby, button_02_start, button_02_copy, label_02_players, lst_02_players)

    # Sheet 3 - lobby (player)
button_03_leave = tk.Button(start_menu.win, CNF_MENU_BUTTON, text='Leave')
button_03_leave.grid(CNF_LABEL_G, row=13, column=38, columnspan=10)

start_menu.add_sheet(3, lst_02_players, button_03_leave, label_02_lobby, label_02_players)

##### Second window - player nickname choose
middle_screen = Window('middle', TITLE, start_menu, Params.color_BG)

    # Adding the stuff that will be always visible
label_1_message = tk.Label(middle_screen.win, bg=Params.color_BG, fg=Params.color_warning, font=Params.font_head)

label_1_message.grid(CNF_LABEL_G, row=7, column=2, columnspan=46)

    # 0 sheet - client
label_10_address = tk.Label(middle_screen.win, CNF_LABEL, text='IP-Address', font=Params.font_middle)
entry_10_ip_address = tk.Entry(middle_screen.win, font=Params.font_middle, bg='CadetBlue1')
button_10_join = tk.Button(middle_screen.win, CNF_MENU_BUTTON, text='Join')
button_10_back = tk.Button(middle_screen.win, CNF_MENU_BUTTON, text='Back')

label_10_address.grid(CNF_LABEL_G, row=2, column=2, columnspan=11)
entry_10_ip_address.grid(CNF_LABEL_G, row=2, column=14, columnspan=16)
button_10_join.grid(CNF_LABEL_G, row=2, column=31, columnspan=8)
button_10_back.grid(CNF_LABEL_G, row=2, column=40, columnspan=8)

middle_screen.add_sheet(0, entry_10_ip_address, label_10_address, button_10_join, button_10_back)

    # 1 sheet - nickname choose
entry_11_nickname = tk.Entry(middle_screen.win, font=Params.font_middle, bg='CadetBlue1')
label_11_nickname = tk.Label(middle_screen.win, CNF_LABEL, text='Nickname', font=Params.font_middle)
button_11_save = tk.Button(middle_screen.win, CNF_MENU_BUTTON, text='Save')
button_11_back = tk.Button(middle_screen.win, CNF_MENU_BUTTON, text='Back')

entry_11_nickname.grid(CNF_LABEL_G, row=2, column=14, columnspan=16)
label_11_nickname.grid(CNF_LABEL_G, row=2, column=2, columnspan=11)
button_11_save.grid(CNF_LABEL_G, row=2, column=31, columnspan=8)
button_11_back.grid(CNF_LABEL_G, row=2, column=40, columnspan=8)

middle_screen.add_sheet(1, entry_11_nickname, label_11_nickname, button_11_save, button_11_back)

##### Third window - game itself
game_screen = Window('game', TITLE, start_menu, Params.color_dark_blue) # 1400x900 - 140 x 90

    # Always visible widgets
tk.Label(game_screen.win, bg=Params.color_BG).grid(row=0, column=0, rowspan=90, columnspan=110, sticky='NSEW')

    # Sheet 0 - Poker table
label_20_table = tk.Label(game_screen.win, image=WImage(game_screen, DIR + r'\gfx\misc\table.png'))
label_20_players = tk.Label(game_screen.win, text='Players', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
label_20_line = tk.Label(game_screen.win, bg=Params.color_white)
label_20_chat = tk.Label(game_screen.win, text='Chat', bg=Params.color_dark_blue, font=Params.font_head, fg=Params.color_white)
label_20_msgs = tk.Label(game_screen.win, text='Abaccio: hey yo hey ya\n\n'*10, font=Params.font_players, anchor='nw', bg=Params.color_dark_blue, fg=Params.color_gold)
#TODO: ^^^ redo as canvas and keep messages in another container variable
''' PASS, CHECK, FOLD, QUIT, CALL, BET, RAISE '''

lst_20_players_nicknames = [
    tk.Label(game_screen.win, text='', font=Params.font_players, anchor='w',
    bg=Params.color_dark_blue, fg=Params.color_gold) for i in range(8)]

# button_20_pass = tk.Button(game_screen.win, cnf_menu_button, text='')
# button_20_check = tk.Button(game_screen.win, cnf_menu_button, text='')
# button_20_fold = tk.Button(game_screen.win, cnf_menu_button, text='')
# button_20_quit = tk.Button(game_screen.win, cnf_menu_button, text='')
# button_20_call = tk.Button(game_screen.win, cnf_menu_button, text='')
# button_20_bet = tk.Button(game_screen.win, cnf_menu_button, text='')
# button_20_raise = tk.Button(game_screen.win, cnf_menu_button, text='')

# button_20_pass.grid(cnf_game_button_g, row=7, column=25, columnspan=9)
# button_20_check.grid(cnf_game_button_g, row=71, column=35, columnspan=9)
# button_20_fold.grid(cnf_game_button_g, row=71, column=45, columnspan=9)
# button_20_quit.grid(cnf_game_button_g, row=71, column=55, columnspan=9)
# button_20_call.grid(cnf_game_button_g, row=71, column=65, columnspan=9)
# button_20_bet.grid(cnf_game_button_g, row=71, column=75, columnspan=9)
# button_20_raise.grid(cnf_game_button_g, row=71, column=85, columnspan=9)

#TODO: seats

label_20_table.grid(CNF_IMAGE_G, row=20, column=12, rowspan=39, columnspan=86)
label_20_players.grid(CNF_LABEL_G, row=0, column=110, columnspan=30)
label_20_line.place(x=1122, y=468, width=256, height=2)
label_20_msgs.grid(row=54, column=110, rowspan=30, columnspan=50)

game_screen.add_sheet(0, label_20_table, label_20_players)


game_screen.enable_debug()



# Deeds
_message_id = None

def message(msg: str):
    global _message_id
    if label_1_message['text'] != '':
        middle_screen.win.after_cancel(_message_id)
    label_1_message['text'] = msg
    _message_id = middle_screen.win.after(4500, lambda: label_1_message.configure(text=''))

def change_nickname(initial: bool = False):
    def confirm():
        if not entry_11_nickname.get():
            message('Enter a valid nickname')
            return
        player_parameters['Name'] = entry_11_nickname.get()
        switch_windows(middle_screen, start_menu, 0)

    entry_11_nickname.delete(0, tk.END)
    entry_11_nickname.insert(0, player_parameters['Name'])
    button_11_save.configure(command=confirm)
    button_11_back.configure(command=lambda: switch_windows(middle_screen, start_menu, 0))

    if initial: # initial=True is called once at start of the game
        button_11_back.configure(state='disabled')
    else:
        button_11_back.configure(state='normal')
    switch_windows(start_menu, middle_screen, 1)

def initial_nickname_check():
    if player_parameters['Name'] == '':
        change_nickname(True)

def host_game(game: Literal['Poker', 'Durak']):
    def disconnect_player(conn: socket.socket):
        print(f'* Player {client_connections[conn]} disconnected (connection lost)')
        readers.remove(conn)
        if conn in listeners:
            listeners.remove(conn)
        if conn in client_connections:
            client_connections.pop(conn)
        conn.close()

    game_parameters['Game'] = game
    if game != 'Omaha':
        button_02_omaha.grid_remove()

    start_menu.show(2)
    trigger_is_closed, trigger_is_started = BoolTrigger(), BoolTrigger()
    button_02_close.configure(command=trigger_is_closed.toggle)
    button_02_start.configure(command=trigger_is_started.toggle)

    sock = socket.socket()
    sock.bind(('', PORT))
    sock.listen(10)

    client_connections: dict[socket.socket, str] = {sock : player_parameters['Name']}
    readers, listeners = [sock], []
    lst_to_read: list[socket.socket]
    lst_to_send: list[socket.socket]

    players_connected = 1

    while not (trigger_is_closed or trigger_is_started):
        lst_to_read, lst_to_send, lst_faults = select.select(readers, listeners, [], 0.016) # ~ 60 fps lol
        for conn in lst_to_read:
            if conn == sock:                                    # new connection recieved
                player, address = sock.accept()
                if players_connected == 8:
                    sendobj(player, CODE_SERVER_FULL)
                player.setblocking(0)
                print('* Recieved connection from address {0}:{1}'.format(*address))
                readers.append(player)
            else:
                data = recvobj(conn)
                if not data:
                    continue
                elif isinstance(data, str) and data not in client_connections.values():
                    if not sendobj(conn, CODE_SUCCESS):         # == if <successfully sent>
                        client_connections[conn] = data
                        listeners.append(conn)
                        players_connected += 1
                        continue
                if data in client_connections.values():
                    sendobj(conn, CODE_NAME_EXISTS)             # disconnection reason
                elif data == CODE_DISCONNECT:
                    sendobj(conn, data)                         # --||--
                disconnect_player(conn)

        for conn in lst_to_send:
            if conn == sock:
                continue
            if not sendobj(conn, client_connections):
                disconnect_player(conn)

        for i in range(8):
            lst_02_players[i]['text'] = [*client_connections.values()][i] if i < players_connected else ''

        start_menu.win.update()

    if trigger_is_closed:                                       # "Close" button pressed
        for conn in client_connections:
            if conn == sock:
                continue
            sendobj(conn, CODE_SHUT_CONN)
            conn.close()
        sock.close()
        switch_windows(middle_screen, start_menu, 0)
        return

    for conn in client_connections:                             # Game start
        if conn == sock:
            continue
        sendobj(conn, client_connections)
    poker_session(client_connections, sock, True)

def join_game():
    #BIG NOTE
    # You can't do stuff with widgets while in thread, so it's desirable that
        # all the parameters which depend on tk Window(s) will be given as arguments;
    # Since there's a loop further down which checks [sock] condition (None, 0 or socket),
        # you can't also change it before it may be changed again.
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
                message(answer.exception)
            else:
                sock = sock_attempt
                return
        except TimeoutError:
            message('Connection attempt timed out')
        except ConnectionRefusedError:
            message('Couldn\'t connect')
        button_10_join.configure(state='normal')
        button_10_back.configure(state='normal')
        sock = 0

    def run_thread():
        ip = entry_10_ip_address.get()
        thread = thr.Thread(target=connection_attempt, args=(ip,))
        thread.start()

    button_10_back.configure(command=lambda:
        trigger_left.toggle() or switch_windows(middle_screen, start_menu, 0))

    button_10_join.configure(command=run_thread)
    switch_windows(start_menu, middle_screen, 0)

    trigger_left = BoolTrigger()
    while not trigger_left:                     # while still on "join - back" sheet
        sock: socket.socket = None
        while sock is None and not trigger_left:
            middle_screen.win.update()

        if trigger_left:                        # left while trying to connect
            sendobj(sock, CODE_DISCONNECT)
            recvobj(sock)
            break

        if not sock:
            continue



        switch_windows(middle_screen, start_menu, 3)
        trigger_game_started, trigger_left_lobby = BoolTrigger(), BoolTrigger()

        while not (trigger_game_started or trigger_left_lobby):
            data: Union[dict[socket.socket, str], GameCode] = recvobj(sock)
            if not isinstance(data, GameCode):
                client_connections = data
                _names_lst = [*client_connections.values()]
                [lst_02_players[i].configure(text = (_names_lst + [''] * 8)[i]) for i in range(8)]
            elif data == CODE_SHUT_CONN: # host closed lobby
                trigger_left_lobby.toggle()
            else: # data == CODE_SUCCESS - game starts
                trigger_game_started.toggle()

            start_menu.win.update()

        if trigger_left_lobby:
            switch_windows(start_menu, middle_screen, 0)
            message('Game closed')
            continue

        client_connections = recvobj(sock)
        if not client_connections: # he fell off while continuing to game :(
            switch_windows(start_menu, middle_screen, 0)
            message('Connection lost')
            continue
        result = poker_session(client_connections, sock)
        #TODO: further depends on result

    return


def poker_session(connections: dict[socket.socket, str], sock: socket.socket, host: bool = False):
    for place, conn in enumerate(connections):
        lst_20_players_nicknames[place]['text'] = f'▶ {connections[conn]}'
        lst_20_players_nicknames[place].grid(CNF_LABEL_G, row = 5*(place + 1), column=112, columnspan=20)

    switch_windows(start_menu, game_screen, 0)

    [Card(game_screen, (ORDER[8 + i], DIAMOND), small=True).grid(row=33, column=33 + 9*i) for i in range(5)]
    # card positions ^^^^^

    #TODO:
    # if host -> ...
    # else -> ...
    # proceed into game
    #
    # * Create Players from cc list
    # * Shuffle Players list (prolly move to the PokerTable game method)
    # * Start the game
    #





def main():
    start_menu.show(0)
    # game_screen.show(0)
    initial_nickname_check()
    start_menu.mainloop()

if __name__ == '__main__':
    main()