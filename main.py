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
    font=Fonts.C14B, fg='yellow', bg=Colors.BG)

label_00_heading.place(x=10, y=10, width=480, height=40)

# 1 layer - menu
button_00_menu_host_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Host game', command=lambda: win_menu.show(layer_0_game_choice))
button_00_menu_join_game = tk.Button(win_menu.win, CNF_MENU_BUTTON,
    text='Join game', command=lambda: on_lobby_enter())
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
    win_menu.win, text='LOBBY', fg='yellow', font=Fonts.C14B, bg=Colors.BG)
label_02_players = tk.Label(
    win_menu.win, CNF_LABEL, text='Players:', font=Fonts.C14B, anchor='w')
label_02_omaha = tk.Label(
    win_menu.win, CNF_LABEL, anchor='w', text='Omaha', font=Fonts.C12B)
label_02_server = tk.Label(
    win_menu.win, CNF_LABEL, text=f'Your IP-address is {IP}',
    font=Fonts.C12B, anchor='w')

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
            anchor='w', font=Fonts.C14B, relief='raised', padx=7
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
button_02_close. place(width=100, height=40, x=380, y=180)

layer_0_lobby_host = GUIWindowLayer(
    win_menu, [
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
    win_middle.win, bg=Colors.BG, fg=Colors.WARNING, font=Fonts.C14B)
label_1_message.place(width=460, height=40, x=20, y=70)

# 1 layer - pre-connection
label_10_address = tk.Label(
    win_middle.win, CNF_LABEL, text='IP-Address', font=Fonts.C12B)
entry_10_ip_address = GUIModernEntry(win_middle.win, CNF_ENTRY)
button_10_join = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Join')
button_10_back = tk.Button(win_middle.win, CNF_MENU_BUTTON, text='Back')

label_10_address.   place(width=110, height=40, x=20, y=20)
entry_10_ip_address.place(width=160, height=40, x=140, y=20)
button_10_join.     place(width=80, height=40, x=310, y=20)
button_10_back.     place(width=80, height=40, x=400, y=20)

layer_1_connection = GUIWindowLayer(
    win_middle,
    [entry_10_ip_address, button_10_back, label_10_address, button_10_join])

# 2 layer - nickname change
entry_11_nickname = GUIModernEntry(win_middle.win, CNF_ENTRY)
label_11_nickname = tk.Label(
    win_middle.win, CNF_LABEL, text='Nickname', font=Fonts.C12B)
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
    win_game.win, text='Players',
    bg=Colors.DBLUE, font=Fonts.C14B, fg=Colors.WHITE)
label_20_chat = tk.Label(
    win_game.win, text='Chat',
    bg=Colors.DBLUE, font=Fonts.C14B, fg=Colors.WHITE)
label_20_line = tk.Label(win_game.win, bg=Colors.WHITE)
canvas_20_chat = tk.Canvas(
    win_game.win, bg=Colors.PITCH_BLACK,
    highlightcolor=Colors.GOLD, scrollregion=(0, 0, 230, 300),
    yscrollcommand=lambda f, l: scrollbar_20.set(f, l))
scrollbar_20 = tk.Scrollbar(
    win_game.win, orient='vertical', command=canvas_20_chat.yview)

entry_20_chat = GUIModernEntry(
    win_game.win, bg=Colors.GREY, fg=Colors.PITCH_BLACK, font=Fonts.H10B)
button_20_msgsend = tk.Button(
    win_game.win, text='▶', font=('Helvetica', '30', 'bold'),
    foreground=Colors.DBLUE)

def _1(i):
    label = tk.Label(
        win_game.win, font=Fonts.H12B,
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
        label_20_table, label_20_players, label_20_chat, label_20_line,
        canvas_20_chat, scrollbar_20, entry_20_chat, *lst_20_nicknames,
        slider_20_betting, button_20_msgsend, button_20_check,
        button_20_call, button_20_show, button_20_bet, button_20_raise,
        button_20_fold, button_20_muck, button_20_quit, button_20_leave
    ]
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Functionality ahead
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class MiddleMessage:
    _last_id = ...
    def __new__(cls, msgtext: str):
        if label_1_message['text'] != '':
            win_middle.win.after_cancel(cls._last_id)

        label_1_message['text'] = msgtext
        cls._last_id = win_middle.win.after(
            5000, lambda: label_1_message.configure(text=''))
        return None

    @staticmethod
    def error(msg: T.Union[str, Exception]):
        MiddleMessage(f"Error: {msg}")

def on_lobby_create(game_type: str):
    def net_service():
        def get_names(d: dict):
            return [v['name'] for v in d.values()]

        def on_player_disconnect(conn: s.socket, send = True):
            for lst in (writers, listeners):
                if conn in lst:
                    lst.remove(conn)
            conn.close()
            if send:
                generate({
                    'event': EV_L_UPD_NAMES,
                    'names': get_names(connections),
                    'pending': n_pending > 0
                })

        def on_lobby_cancel():
            for conn in connections:
                if conn == ssock:
                    continue
                Network.send(conn, {'event': EV_L_CLOSED})
                conn.close()
            ssock.close()

        def generate(event: EventType):
            [q.push(event) for q in (queue_inner, queue_out)]

        nonlocal connections
        nonlocal t_cancel, t_start
        ssock = s.socket()
        ssock.bind(('', PORT))
        ssock.listen()

        connections[ssock] = {'name': PlayerData()['name']}
        n_pending = 0
        writers, listeners = [ssock], []
        # Initial update to the player list, adding host themselves
        queue_out.push({
            'event': EV_L_UPD_NAMES,
            'names': [PlayerData()['name']],
            'pending': 0,
        })

        while not (t_cancel
                   or (t_start and not n_pending)
                   or GUIWindow.destroyed):
            lst_read, lst_write, _ = sel.select(writers, listeners, [], 1/60)
            for socket in lst_read:
                if socket is ssock:
                    conn, _ = ssock.accept() #FUTURE: allow reconnect
                    if len(connections) == 8:
                        Network.send(conn, {'event': EV_L_ERR_FULL})
                        conn.close()
                    elif not Network.send(conn, {'event': EV_SUCCESS}):
                        conn.close()
                    else:
                        conn.settimeout(S_TIMEOUT)
                        connections[conn] = {'name': 'connecting...'}
                        n_pending += 1
                        writers.append(conn)
                        generate({
                            'event': EV_L_UPD_NAMES,
                            'names': get_names(connections),
                            'pending': n_pending > 0,
                        })
                    continue

                data: EventType | EventCodeType = Network.answer(socket)

                # Network.answer sent pure error event, disconnect
                if isinstance(data, EventCodeType):
                    on_player_disconnect(socket)
                    continue

                elif isinstance(data, EventType):
                    if data['event'] != EV_L_NAME_SUPPLY \
                        or not Network.ask(socket, EV_SUCCESS):
                        on_player_disconnect(socket)
                        continue

                    connections[conn]['name'] = data['name']
                    n_pending -= 1
                    listeners.append(conn)
                    generate({
                        'event': EV_L_UPD_NAMES,
                        'names': get_names(connections),
                        'pending': n_pending > 0,
                    })
                    continue

                raise Exception(f"Unexpected data '{data}'")

            event: Queue.EMPTY | EventType = queue_inner.get()
            if event is Queue.EMPTY:
                continue

            for socket in lst_write:
                if not Network.ask(socket, event):
                    on_player_disconnect(socket)

        if GUIWindow.destroyed:
            on_lobby_cancel()

        on_lobby_cancel()
        return #TODO

    def on_player_joins_quits(event: EventType):
        for i, name in enumerate(event['names']):
            lst_02_players[i]['text'] = name

        for j in range(i + 1, 8):
            lst_02_players[j]['text'] = ''

        button_02_start['state'] = B_STATES[bool(not event['pending'] and i)]

    queue_inner, queue_out = Queue(), Queue()
    t_cancel, t_start = Trigger(), Trigger()

    button_02_start['state'] = 'disabled'
    button_02_close['command'] = t_cancel.pull
    button_02_start['command'] = t_start.pull

    win_menu.show(
        layer_0_lobby_host,
        hide=[button_02_omaha, label_02_omaha] * (game_type != 'Poker'))

    # main GUI/server loop
    connections: dict[s.socket, dict]  = {}
    worker = thr.Thread(target=net_service, daemon=True)
    worker.start()
    while not (t_cancel or t_start or GUIWindow.destroyed):
        if (event := queue_out.get()) is not Queue.EMPTY:
            on_player_joins_quits(event)
        win_menu.update()

    if GUIWindow.destroyed:
        return

    elif t_cancel:
        GUIWindow.switch_to(win_menu, layer_0_main_menu)
        return

    #TODO game started
    pass

def on_connection_menu_enter() -> tuple[bool, T.Optional[s.socket]]:
    def connection_attempt():
        def thr_connect(ip: str):
            try:
                sock = s.socket()
                sock.settimeout(S_TIMEOUT)
                sock.connect((ip, PORT))
                answer = Network.answer(sock)           # EV_SUCCESS = 0
                if isinstance(answer, EventCodeType) or answer['event']:
                    sock.close()
                    attempt['result'] = answer
                    return

                attempt['result'] = sock
            except Exception as e:
                attempt['result'] = e
            finally:
                attempt['finished'] = True
        pass

        ip = entry_10_ip_address.get()
        if not Network.validate_ip(ip):
            attempt['result'] = Exception('invalid IP supplied')
            attempt['finished'] = True

        button_10_back.configure(state='disabled')
        button_10_join.configure(state='disabled')

        worker = thr.Thread(target=thr_connect, args=(ip,))
        attempt['thread'] = worker
        worker.start()

    attempt = {'thread': None, 'finished': False, 'result': None}

    tr_left = Trigger()
    button_10_back.configure(command=tr_left.pull)
    button_10_join.configure(command=connection_attempt)

    win_menu.switch_to(win_middle, layer_1_connection)

    while not tr_left and not GUIWindow.destroyed:
        if attempt['thread'] and attempt['finished']:
            output = attempt['result']

            if isinstance(output, s.socket):
                return (True, output)

            elif isinstance(output, Exception):
                MiddleMessage.error({
                    ConnectionAbortedError,
                    ConnectionRefusedError,
                    ConnectionResetError,
                    TimeoutError, #TODO:

                }[type(output)])
            elif isinstance(output, (EventCodeType, dict)):
                if type(output) == dict:
                    output = output['event']

                print(f'Received {output}')
                MiddleMessage.error({
                    EV_L_ERR_FULL: 'lobby full',
                    EV_S_ERR_TIMEOUT: 'connection timed out',
                    EV_L_CLOSED: 'lobby closed'
                }[output])

            attempt = {'thread': None, 'finished': False, 'result': None}
            button_10_back['state'] = 'normal'
            button_10_join['state'] = 'normal'

        win_middle.update()

    if GUIWindow.destroyed:
        if (thread := attempt['thread']):
            thread.join()
            if isinstance(sock := attempt['result'], s.socket):
                sock.close()

        return (False, None)

    win_middle.switch_to(win_menu, layer_0_main_menu)
    return (False, None)

def on_lobby_enter():
    def on_player_joins_quits(lst: list):
        [lst_02_players[i].config(text=n) for i, n in enumerate(lst)]

    def on_disconnect(event: EventType):
        pass

    result, socket = on_connection_menu_enter()
    if not result:
        return

# def on_lobby_enter():
#     def on_connmenu_enter() -> tuple[bool, T.Union[s.socket, None]]:
#         """
#         Is called at start.
#         Returns `(True, sock)` if user connects to lobby,
#         `(False, None)` if leaves win_middle
#         """
#         res = {}
#         conn_attempt_made = False
#         def conn_attempt():
#             nonlocal conn_attempt_made
#             ip = entry_10_ip_address.get()
#             if not Network.validate_ip(ip):
#                 res['Result'] = (None, "Error: Invalid IP")
#                 conn_attempt_made = True
#                 return

#             def _(ip: str, name: str):
#                 nonlocal conn_attempt_made
#                 sock = s.socket()
#                 sock.settimeout(3)
#                 try:
#                     sock.connect((ip, PORT))
#                     Network.send(sock, ['join', name])
#                     # GC_SUCCESS is 0, so if successfull, returns sock
#                     res['Result'] = (sock, Network.receive(sock))
#                 except Exception as err:
#                     print(err)
#                     res['Result'] = (sock, err)
#                 finally:
#                     conn_attempt_made = True

#             button_10_back.configure(state='disabled')
#             button_10_join.configure(state='disabled')
#             res['Thread'] = (worker := thr.Thread(target=_, args=(ip,)))
#             worker.start()

#         button_10_join.configure(command=conn_attempt)
#         button_10_back.configure(command=lambda: GUIWindow.switch_to(
#             win_menu, layer_0_main_menu))

#         GUIWindow.switch_to(win_middle, layer_1_connection)

#         while not GUIWindow.destroyed and GUIWindow.current == win_middle:
#             win_middle.update()
#             t.sleep(0.001)
#             if not conn_attempt_made:
#                 continue

#             res.pop('Thread', None) # removing used thread
#             sock, data = res.pop('Result')
#             print(data)

#             if isinstance(data, (Exception, SocketClosed, str)):
#                 MiddleMessage.error({
#                         SocketClosed : "attempt timed out",
#                         TimeoutError: "attempt timed out",
#                         ConnectionRefusedError: "connection refused",
#                         str : data
#                     }.get(type(data), "unknown error"))
#             elif data == 0:
#                 button_10_back.configure(state='normal')
#                 button_10_join.configure(state='normal')
#                 return True, sock # socket connected successfully @exit
#             elif isinstance(data, int):
#                 MiddleMessage.error(
#                     ["lobby closed by host",
#                         "lobby is full"][data == GC_ERR_LOBBY_FULL])
#             else:
#                 raise Exception(f"unexpected value {data = }")

#             button_10_back.configure(state='normal')
#             button_10_join.configure(state='normal')
#             conn_attempt_made = False

#         # left window
#         # to close connection and free socket
#         if 'Thread' in res:
#             while res['Thread'].is_alive:
#                 pass
#             sock: s.socket
#             data: T.Union[Exception, SocketClosed, int]
#             sock, data = res['Result']
#             if isinstance(data, (SocketClosed, int)):
#                 Network.send(sock, GC_DISCONNECT)
#             sock.close()
#         return False, None

#     result, sock = on_connmenu_enter()
#     if not result:
#         return

#     while True:
#         sock.settimeout(0.3)
#         print(Network.receive(sock))
#         win_middle.update()#TODO

#     #TODO game

# def on_lobby_create_old(game: str):
#     def on_player_disconnect(conn: s.socket):
#         [lst.remove(conn) for lst in (writers, listeners) if conn in lst]
#         connections.pop(conn, None)
#         conn.close()
#     def on_lobby_cancel():
#         for conn in connections:
#             if conn is sock: continue
#             Network.send(conn, GC_ERR_LOBBY_CLOSING)
#             conn.close()
#         sock.close()
#         if not GUIWindow.destroyed:
#             GUIWindow.switch_to(win_menu, layer_0_main_menu)
#     list_updated = False
#     def update(n_conns_pending: list[int]):
#         nonlocal list_updated
#         win_menu.update()
#         to_read, to_write, _ = sel.select(writers, listeners, [], 0.001)
#         for conn in lst_read:
#             if conn == sock:
#                 player, address = sock.accept()
#                 if len(connections) == 9:
#                     Network.send(player, GC_ERR_LOBBY_FULL)
#                     player.shutdown()
#                     player.close()
#                     continue
#                 player.settimeout(3)
#                 connections[player] = {'Name': 'connecting...',
#                                        'ID': "{}:{}".format(*address)}
#                 writers.append(player)
#                 n_conns_pending[0] += 1
#                 continue
#             data = Network.receive(conn)
#         lst_read, lst_send, _ = sel.select(writers, listeners, [], 0.001)
#         for conn in lst_read:
#             if conn == sock: # new connection
#                 player, address = sock.accept()
#                 if len(connections) == 9:
#                     Network.send(player, GC_ERR_LOBBY_FULL)
#                     player.close()
#                     continue
#                 player.settimeout(3)
#                 connections[player] = {'Name': 'connecting...',
#                                        'ID': "{}:{}".format(*address)}
#                 writers.append(player)
#                 n_conns_pending[0] += 1
#                 continue
#             data = Network.receive(conn)
#             if data in {FLAG_RECV_EMPTY, FLAG_SOCK_CLOSED}:
#                 on_player_disconnect(conn)
#                 continue
#             match data:
#                 case ['join', name]:
#                     if not Network.send(conn, GC_SUCCESS):
#                         on_player_disconnect(conn)
#                         continue
#                     connections[conn]['Name'] = name
#                     n_conns_pending[0] -= 1
#                     listeners.append(conn)
#                 case ['leave']:
#                     on_player_disconnect(conn)
#         lst_names = [a['Name'] for a in connections.values()]
#         lst_names += [''] * 7
#         for conn in lst_send:
#             if not Network.send(conn, lst_names):
#                 on_player_disconnect(conn)
#         try:
#             [lst_02_players[i].config(text=lst_names[i]) for i in range(8)]
#             button_02_start['state'] = (
#                 B_STATES[bool(n_conns_pending[0] * (len(lst_names) - 1))])
#         except tk.TclError:
#             # in this context it means host left app
#             return on_lobby_cancel()
#     tr_cancelled, tr_started = Trigger(), Trigger()
#     button_02_start.configure(state='disabled')
#     button_02_close.configure(command=tr_cancelled.toggle)
#     button_02_start.configure(command=tr_started.toggle)
#     win_menu.show(
#         layer_0_lobby_host,
#         hide=[button_02_omaha, label_02_omaha] * (game != 'Poker'))
#     sock = s.socket()
#     sock.bind(('', PORT))
#     sock.listen(9)
#     connections = {sock: {'Name' : PlayerData()['name'], 'ID' : 'host'}}
#     writers, listeners = [sock], []
#     n_conns_pending = [0]
#     while not (tr_cancelled or tr_started or GUIWindow.destroyed):
#         update(n_conns_pending)
#     #TODO
#     on_lobby_cancel()

def nickname_change(initial: bool = False):
    def on_keypress(ev):
        win_middle.update()
        button_11_save.configure(
            state='normal' if entry_11_nickname.get() else 'disabled')

    def on_save_attempt():
        PlayerData()['name'] = entry_11_nickname.get()
        win_middle.win.unbind_all('<Key>')
        GUIWindow.switch_to(win_menu, layer_0_main_menu)

    win_middle.win.bind('<Key>', on_keypress)
    entry_11_nickname.delete(0, tk.END)
    entry_11_nickname.insert(0, PlayerData()['name'])

    button_11_save.configure(command=on_save_attempt,
        state=B_STATES[not initial])
    button_11_back.configure(
        command=on_quit
            if initial
                else lambda: GUIWindow.switch_to(win_menu, layer_0_main_menu)
    )
    GUIWindow.switch_to(win_middle, layer_1_nickname)

def initial_nickname_check():
    if PlayerData()['name'] == '':
        nickname_change(True)

def on_quit():
    PlayerData.write()
    GUIWindow.app_quit()

def debug_game():
    for lbl in lst_20_nicknames:
        lbl.configure(text='Test')

    win_game.show(layer_2_poker, True)
    win_game.mainloop()

def main():
    win_menu.show(layer_0_main_menu, True)
    initial_nickname_check()
    win_menu.mainloop()

def game_debug():
    win_game.show(layer_2_poker, True)
    win_game.mainloop()

if __name__ == '__main__':
    try:
        main()
    finally:
        if not GUIWindow.destroyed:
            on_quit()