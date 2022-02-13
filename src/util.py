from functools import reduce
from itertools import combinations as iter_combs
from typing import Literal, Union
from random import shuffle, choice
import urllib.request, urllib.error
import tkinter as tk
import tkinter.font as tkf
import os.path
import socket
import pickle
import json
import time as t
from src.helpers import *

__all__ = [
    # constants
    'SPADE',
    'HEART',
    'CLUB',
    'DIAMOND',
    'SUITS',
    'ORDER',
    'DECK',
    'IP',
    'PORT',
    'DIR',
    'TITLE',
    'DIMS',
    'CODE_NAME_EXISTS',
    'CODE_SHUT_CONN',
    'CODE_SUCCESS',
    'CODE_DISCONNECT',
    'CODE_SERVER_FULL',
    'CNF_MENU_BUTTON',
    'CNF_LABEL',
    'CNF_LABEL_G',
    'CNF_IMAGE_G',
    'CNF_GAME_BUTTON_G',
    'SOCKET_TIMEOUT',

    # modules
    'socket',
    'tk',

    # functions
    'smartify_entry',
    'reduce',
    'shuffle',
    'choice',
    'check_ip_mask',
    'recvobj',
    'sendobj',
    'deal_cards',
    'end_join',
    'holdem_combination',
    'compare_combinations',
    'poker_combination',
    'share_the_pot',
    'switch_windows',

    # variables
    'game_parameters',
    'player_parameters',

    # classes
    'Literal',
    'Union',
    'PokerCombination',
    'Params',
    'WImage',
    'GameCode',
    'BoolTrigger',
    'Window',
    'Card',
    'TableSeat',
    'MyEvent',
    'PokerPlayer',
    'PokerTable',
    'WindowSheet',
    'CanvasChat',
]

# # # # # # # # # # # # # # # # | SERVER | # # # # # # # # # # # # # # # #
def get_ip() -> str:
    try:
        ip = urllib.request.urlopen("https://ident.me", timeout=1).read().decode("utf8")
    except urllib.error.URLError:
        ip = socket.gethostbyname(socket.gethostname())
    return ip

@exception_proof_ish(True)
def recvobj(sock_where: socket.socket):
    '''Recieve an object from `sock_where`\n\n return None on success'''
    objlen = sock_where.recv(HEADLEN).decode()
    if not objlen:
        return None
    objlen = int(objlen)
    res = b''
    while len(res) < objlen:
        res += sock_where.recv(min(2048, objlen - len(res)))
    # a = pickle.loads(res)
    # print('got', a)
    # return a
    return pickle.loads(res)

@exception_proof_ish(True)
def sendobj(sock_where: socket.socket, obj):
    '''Send object `obj` to `sock_where`\n\nreturn None on success'''
    # print('sent', obj)
    obj = pickle.dumps(obj)
    obj = str(len(obj)).zfill(HEADLEN).encode() + obj
    return sock_where.sendall(obj)

# # # # # # # # # # # # # # # # | POKER | # # # # # # # # # # # # # # # #
def deal_cards(player_count, game_type):
    return [choice(DECK) for i in range(player_count*(2 + 2*(game_type)) + 5)]

def holdem_combination(cards: list['Card']) -> PokerCombination:
    '''Return the best possible Texas Hold'em Poker hand of available with input cards\n```
    | 10 - Flush Royale | 9 - Straight flush
    | 8 - Four          | 7 - Full House
    | 6 - Flush         | 5 - Straight
    | 4 - Set           | 3 - Two pairs
    | 2 - Pair          | 1 - Higher card
    '''
    def order_range(start, stop):
        i = start
        while i < stop:
            yield ORDER[i]
            i += 1

    cards = sorted(cards, key=lambda card: ORDER.index(card[0]), reverse=True)
    nominals : list; suits: list
    nominals, suits = zip(*cards)
    nominal_quantities = {elem : nominals.count(elem) for elem in set(nominals)}
    suit_quantities = {elem : suits.count(elem) for elem in set(suits)}
    result = PokerCombination()
    if any(suit_quantities[x] >= 5 for x in suit_quantities): # 10 - 9 - 6
        main_suit = [suit for suit in suit_quantities if suit_quantities[suit] >= 5][0]
        filtered_cards, _ = zip(*[card for card in cards if card[1] == main_suit])
        for i in range(len(ORDER) - 5, -2, -1): # 10 - 9
            if all([*order_range(i, i + 5)][::-1][n] in filtered_cards for n in range(5)):
                if i == len(ORDER) - 5: # 10
                    result.name = f'Flush Royale: A to 10 of {main_suit}'
                    result.hand = [10]
                else: # 9
                    result.name = f'Straight Flush: {ORDER[i + 4]} to {ORDER[i]} of {main_suit}'
                    result.hand = [9, i + 4]
                return result
        result.name = f"Flush: {' '.join([str(f) for f in filtered_cards])} of {main_suit}" # 6
        result.hand = [6] + [ORDER.index(el) for el in filtered_cards[:5]]

    if 4 in nominal_quantities.values(): # 8
        main_nominal = [a for a in nominal_quantities if nominal_quantities[a] == 4][0]
        result.name = f'Four of {main_nominal}\'s'
        result.hand = [8, ORDER.index(main_nominal)]
        result.kicker = [ORDER.index(a) for a  in nominals[4:]][:1]
        return result

    if 3 in nominal_quantities.values() and result.hand[0] <= 4: # 7 - 4
        set_nominals = sorted([x for x in nominal_quantities if nominal_quantities[x] == 3], key=ORDER.index)
        pair_nominals = sorted([x for x in nominal_quantities if nominal_quantities[x] == 2], key=ORDER.index)
        if len(pair_nominals):
            main_nominal = set_nominals[-1]
            max_pairs_nominal = max([x for x in pair_nominals + set_nominals[:-1]], key=ORDER.index)
            result.name = f'Full House: set of {main_nominal} and a pair of {max_pairs_nominal}'
            result.hand = [7, ORDER.index(main_nominal), ORDER.index(max_pairs_nominal)]
            return result
        result.name = f'Set of {set_nominals[0]}'
        result.hand = [4, ORDER.index(set_nominals[0])]
        result.kicker = [ORDER.index(a) for a in nominals if a != set_nominals[0]][:2]

    for i in range(len(ORDER) - 5, -2, -1): # 5
        if all([*order_range(i, i + 5)][::-1][n] in nominals for n in range(5)):
            result.name = f'Straight: {ORDER[i + 4]} to {ORDER[i]}'
            result.hand = [5, i + 4]
            return result

    if 2 in nominal_quantities.values() and result.hand[0] < 1: #3 - 2
        pair_nominals = sorted([x for x in nominal_quantities if nominal_quantities[x] == 2], key=ORDER.index)
        if len(pair_nominals) > 1:
            result.name = f'Two pairs: a pair of {pair_nominals[-1]} and a pair of {pair_nominals[-2]}'
            result.hand = [3] + [ORDER.index(a) for a in pair_nominals[-2:][::-1]]
            result.kicker = [ORDER.index(a) for a in nominals if a not in pair_nominals[-2:]][:1]
        else:
            result.name = f'Pair of {pair_nominals[0]}'
            result.hand = [2] + [ORDER.index(pair_nominals[0])]
            result.kicker = [ORDER.index(a) for a in nominals if a != pair_nominals[0]][:3]
        return result

    if result.hand[0] == 0:
        result.name = f'Higher card: {nominals[0]}'
        result.hand, result.kicker = (lambda a: ([a[0]], a[1:]))([ORDER.index(card) for card in nominals[1:]][:5])
    return result

def compare_combinations(combinations: list[PokerCombination]) -> PokerCombination:
    '''Return best combination of `combinations`'''
    current = combinations[0]
    for comb in combinations[1:]:
        if comb.hand > current.hand:
            current = comb
        elif comb.hand == current.hand:
            if not comb.kicker or comb.kicker > current.kicker:
                current = comb
    return current

def poker_combination(player_cards: list['Card'], table_cards: list['Card'], game_type: Literal[0, 1]) -> PokerCombination:
    if game_type == 0:
        return holdem_combination(player_cards + table_cards)
    player_card_variants = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    if not len(table_cards):
        return compare_combinations([holdem_combination([player_cards[i] for i in p_var]) for p_var in player_card_variants])
    result: list[PokerCombination] = []
    table_card_variants = [*iter_combs(range(len(table_cards)), 3)]
    for p_var in player_card_variants:
        for t_var in table_card_variants:
            result.append(holdem_combination([player_cards[i] for i in p_var] + [table_cards[j] for j in t_var]))
    return compare_combinations(result)

def share_the_pot(pot, *players: 'PokerPlayer') -> int:
    '''Share pot between players'''
    for p in players:
        p.bankroll += pot // len(players)

# # # # # # # # # # # # # # # # # # | MAIN | # # # # # # # # # # # # # # # # # #
IP, PORT = get_ip(), 50240
DIR = '\\'.join(__file__.split('\\')[:-2])
TITLE = 'Tony\'s Card Games Catalogue'
DIMS = {
    'menu': (500, 600),
    'middle': (500, 130),
    'game' : (1400, 900)
}

game_parameters = {
    'Game' : None,            # Poker - Durak
    'Player count' : None     # 2 - 8
}

if os.path.exists(DIR + r'\util\player.json'):
    player_parameters: dict[Literal['Name', 'IP'], str] = json.load(open(DIR + r'\util\player.json'), 'r')
else:
    player_parameters = {'Name' : '', 'IP' : ''}

class WImage:
    '''``cached tk.PhotoImage'''
    cache = []
    def __new__(cls, master: 'Window', file) -> 'WImage':
        instance = tk.PhotoImage(master=master.win, file=file)
        cls.cache.append(instance)
        return instance

class WindowSheet:
    def __init__(self, master: 'Window', grid_items: list[tk.Widget] = None, place_items: list[tk.Widget] = None) -> None:
        self.grid_collection: list[tk.Widget] = []
        self.place_collection: dict[tk.Widget, dict[str, ]] = {}
        if grid_items:
            self.add_grid(*grid_items)
        if place_items:
            self.add_place(*place_items)
        master._sheets.append(self)

    def add_grid(self, *items):
        self.grid_collection += reduce(lambda res, a: res + [a] if not isinstance(a, list) else res + a, items, [])
        self.hide()

    def add_place(self, *items):
        items_lst: list[tk.Widget] = reduce(lambda res, a: res + [] if not isinstance(a, list) else res + a, items, [])
        self.place_collection = {**{a: a.place_info() for a in items_lst}, **self.place_collection}

    def hide(self): [elem.grid_remove() for elem in self.grid_collection]
    def show(self): [elem.grid() for elem in self.grid_collection]
    def disable(self): [elem.configure(state='disabled') for elem in self.grid_collection]
    def enable(self): [elem.configure(state='normal') for elem in self.grid_collection]

class Window:
    current_window = None
    quit = 0
    __ins: list["Window"] = []

    @classmethod
    def quit_window(cls):
        BoolTrigger.disable()
        for w in Window.__ins:
            w.win.destroy()
        Window.quit = True

    def __init__(self, name: str, title: str, master: 'Window' = ..., bg: str = None) -> None:
        self._sheets: list[WindowSheet] = []
        self._size = DIMS[name]
        self.win = tk.Tk() if master == ... else tk.Toplevel(master.win)
        self.win.protocol('WM_DELETE_WINDOW', Window.quit_window)
        self.win.resizable(0, 0)
        self.win.title(title)
        a, b = (self.win.winfo_screenwidth() - self._size[0]) // 2, (self.win.winfo_screenheight() - self._size[1]) // 2
        self._geometry = f'{self._size[0]}x{self._size[1]}+{a}+{b}'
        self.win.geometry(self._geometry)
        self.current_sheet = None
        if bg != None: self.win['bg'] = bg
        self._hidden: bool = False

        for column in range(self._size[0] // 10):
            self.win.columnconfigure(column, weight=1, minsize=10)
        for row in range(self._size[1] // 10):
            self.win.rowconfigure(row, weight=1, minsize=10)
        self.hide()
        if master == ...:
            Window.__ins.append(self)

    def _show_sheet(self, sheet: WindowSheet):
        [sh.hide() for sh in self._sheets if sh != sheet]
        sheet.show()

    def hide(self):
        self.win.withdraw()
        self._hidden = True

    def show(self, sheet: WindowSheet):
        if self._hidden:
            self.win.geometry(self._geometry)
            self._hidden = not self._hidden
        self._show_sheet(sheet)
        self.current_sheet = sheet
        self.win.deiconify()
        self.win.focus_set()
        __class__.current_window = self

    def mainloop(self): self.win.mainloop()

    def enable_debug(self):
        column = lambda e: (e.x + (e.widget.winfo_x() if e.widget != self.win else 0))
        row = lambda e: (e.y + (e.widget.winfo_y() if e.widget != self.win else 0))
        self.win.bind('<Button-3>', lambda e: print(f'x (column): {column(e)}, y (row): {row(e)}'))

def switch_windows(from_: Window, to: Window, which: int):
    from_.hide()
    to.show(which)
    Window.current_window = to

def smartify_entry(entry: tk.Entry):
    def copy(entry: tk.Entry):
        if entry.select_present():
            entry.clipboard_clear()
            entry.clipboard_append(entry.selection_get())

    def paste(entry: tk.Entry):
        if entry.select_present():
            start = entry.index(tk.SEL_FIRST)
            end = entry.index(tk.SEL_LAST)
        else:
            start = entry.index(tk.INSERT)
            end = entry.index(tk.INSERT)

        entry.delete(start, end)

        try:
            entry.insert(start, entry.master.clipboard_get())
        except tk.TclError:
            entry.insert(start, '')

    def cut(entry: tk.Entry):
        if entry.select_present():
            start = entry.index(tk.SEL_FIRST)
            end = entry.index(tk.SEL_LAST)
            entry.clipboard_append(entry.get()[start:end])
            entry.delete(start, end)

    def sel_all(entry: tk.Entry):
        entry.select_range(0, tk.END)

    keybinds = {
        67: copy,
        86: paste,
        88: cut,
        65: sel_all
    }

    def ctrl_keyhandler(ev: tk.Event):
        if ev.keycode in keybinds:
            keybinds[ev.keycode](ev.widget)

    entry.bind(f'<Control-Key>', ctrl_keyhandler)
    return entry

class CanvasChat:
    LETTER_HEIGHT = 20

    def __init__(self, coords: tuple[int, int], canv: tk.Canvas, font, fill, width) -> None:
        self.canv = canv
        self.x, self.y = coords
        self.font = tkf.Font(self.canv, font)
        self.max_llen = width - self.x
        self.fill = fill

    def add_line(self, line: str):
        colors = {
            'BLUE'      : '#55F',
            'RED'       : '#F55',
            'PURPLE'    : '#608',
            'YELLOW'    : '#FF1',
            'GREEN'     : '#1F1',
            ''          : self.fill
        }

        x, y = self.x, self.y
        color = self.fill

        while line:                                             #cycle thru all the line chars
            char = line[0]
            line = line[1:]

            if char == '{':
                while char[-1] != '}':
                    char += line[0]
                    line = line[1:]
                col = char[1:][:-1]                             # trim brackets
                if col in colors:                               #DO possibilities for other tags
                    color = colors[col]
                continue

            if self.font.measure(char) + x + 1 > self.max_llen:
                x = self.x
                y += self.LETTER_HEIGHT + 2

            self.canv.create_text(x, y, text=char, anchor='nw', justify='left', font=self.font, fill=color)
            x += self.font.measure(char) + 1

        y += self.LETTER_HEIGHT + 5
        self.y = y

class Card:
    def __init__(self, master: 'Window', card_value: tuple[Union[int, str], str], shirt_up: bool = False, small: bool = False) -> None:
        self.rank, self.suit = card_value
        self.master = master
        self.shirt_up = shirt_up
        file = DIR + r'\gfx\cards\\' + str(DECK.index(card_value)) + ('.png' if not small else '_small.png')
        self.label = tk.Label(master.win, image=WImage(self.master, file))

    def grid(self, row: int, column: int) -> None:
        self.label.grid(row=row, column=column, rowspan=13, columnspan=8, sticky='NWES')

    def __repr__(self) -> str:
        return f'<Card, {self.rank} of {self.suit}>'

    def __getitem__(self, val):
        return [self.rank, self.suit][val]

class TableSeat:
    coords = { #pixel positions of all player "equipment" - chips, cards and real cards positions for showing #TODO: card positions (after seat graphics)
        0 : {'table': (216, 306), 'cards': (0, 0), 'chips': ((27, 28), (26, 28), (25, 29)), 'seat': (0, 0)}, # blue, green, red ("rgb backwards")
        1 : {'table': (436, 264), 'cards': (0, 0), 'chips': ((51, 28), (51, 27), (50, 27)), 'seat': (0, 0)},
        2 : {'table': (616, 264), 'cards': (0, 0), 'chips': ((70, 27), (69, 27), (68, 27)), 'seat': (0, 0)},
        3 : {'table': (818, 306), 'cards': (0, 0), 'chips': ((83, 28), (83, 29), (84, 29)), 'seat': (0, 0)},
        4 : {'table': (813, 420), 'cards': (0, 0), 'chips': ((82, 50), (83, 50), (84, 49)), 'seat': (0, 0)},
        5 : {'table': (616, 472), 'cards': (0, 0), 'chips': ((67, 50), (68, 50), (69, 51)), 'seat': (0, 0)},
        6 : {'table': (436, 472), 'cards': (0, 0), 'chips': ((39, 51), (40, 51), (41, 51)), 'seat': (0, 0)},
        7 : {'table': (216, 416), 'cards': (0, 0), 'chips': ((26, 49), (27, 49), (27, 50)), 'seat': (0, 0)}
    }
    def __init__(self, master: Window, place: int, *cards: Card) -> None:
        self.place, self.cards = place, cards
        file = DIR + fr"\gfx\cards\cards{'_down' if self.place in [0, 4] else '_up' if self.place in [3, 7] else ''}.png"
        self.cards_label = tk.Label(master.win, image=WImage(master, file))

        width, height = ((66, 69) if self.place in [3, 7] else ((71, 66) if self.place in [0, 4] else (48, 55)))
        self.tokens = [tk.Label(master.win, image=WImage(master, DIR + rf'\gfx\tokens\token {color}.png')) for color in ['blue', 'green', 'red']]
        x, y = TableSeat.coords[self.place]['table']
        self.place_params = {'x' : x, 'y' : y, 'width' : width, 'height' : height}

    def show_table_cards(self):
        '''show cards on the table'''
        self.cards_label.place(**self.place_params)

    def display_tokens(self, num: int):
        for token in self.tokens:
            token.grid_remove()
        for i in range(num):
            x, y = TableSeat.coords[self.place]['chips'][i]
            self.tokens[i].grid(row=y, column=x, rowspan=1, columnspan=1, sticky="NWES")

    def hide_cards(self):'''hide cards from the table'''
    def show_player_cards(self): '''show REAL cards'''

class PokerPlayer:
    def __init__(self, name: str, place: int, conn: socket.socket):
        self.name, self.conn = name, conn
        self.place, self.seat = TableSeat(place), place
        self.current_bet = 0
        self.did_move = False
        self.is_dealer = False
        self.set_default()

    def set_default(self):
        self.is_out = False # player folded or quit
        self.bankroll = 1000
        self.cards = []

    def action(self, bet=0, small_blind=10):
        self.did_move = True
        options = []
        if bet <= self.current_bet:
            options.append('check')
        elif self.bankroll > bet:
            options.append('call')
        else:
            options.append('all-in')
        if bet == 0:
            options.append('bet')
        elif self.bankroll > bet*2:
            options.append('raise')
        options.extend(['fold', 'quit'])

        answer = True #DO send request
        #DO:
        if answer == 'check':
            # bet stays the same
            '''player calls'''
        elif answer == 'call':
            self.current_bet = bet
            '''player calls'''
        #DO
        elif answer in "FQ": # messages
            self.is_out = True
            if answer == "Q":
                self.bankroll = 0
        elif answer == "A":
            self.bet(self.bankroll)
        elif answer in 'BR':
            minimum = max(bet, small_blind * 4) if answer == "R" else small_blind * 2
            new_bet: int # get a new bet
            self.bet(new_bet)








    def bet(self, bet: int, sb=False, bb=False):
        pass#TODO:

class PokerTable:
    def __init__(self, *players: PokerPlayer, event_manager) -> None:
        self.players = players

    def set_default(self): [p.set_default for p in self.players]

    def party(self, small_blind, game_type):
        def check_the_bets(bet: int):
            '''All the players did move, called or all-in'd or folded'''
            return all([p.did_move and (p.current_bet in [bet, p.bankroll] or p.is_out) for p in self.players])

        def ask(player: PokerPlayer, table_cards: tuple[Card]):
            comb = poker_combination(player.cards, table_cards, game_type)
            #DO display who's move it is
            # send a request to show their cards or muck
            if 'yes':
                ... #DO show their cards and comb to everybody
                return player, comb
            else:
                ... #DO player mucks cards

        sits = len(self.players)
        game_type = (game_type == 'Omaha')
        game_state = 0
        current_pot = 0
        dealer_place = [a.place for a in self.players if a.is_dealer][0]
        table_cards = deal_cards(sits, game_type)
        self.set_default()

        def active_players(): return [p for p in self.players if not p.is_out]

        for player in self.players:
            [player.cards.append(table_cards.pop(0)) for i in range(1 + game_type)]

        while game_state < 4 and len(active_players()) > 1:
            #DO send game info to every player
            bet = 0
            if game_state == 0:
                #DO sb, bb
                self.players[(dealer_place + 1) % sits].bet(small_blind, sb=True)
                self.players[(dealer_place + 2) % sits].bet(small_blind * 2, bb=True)
                bet = max([a.current_bet for a in self.players])
                counter = (dealer_place + 3) % sits

            while (counter < len(self.players) or not check_the_bets(bet)) and len(active_players()) > 1:
                current_player = self.players[counter % sits]
                if current_player.bankroll and not current_player.is_out:
                    #DO inform others
                    current_player.action(bet, small_blind)
                bet = max(bet, current_player.current_bet)
                counter += 1

            for player in self.players:
                player.did_move = False
                if bet > 0:
                    current_pot += player.current_bet
                    player.bankroll -= player.current_bet
                    player.current_bet = 0

            game_state += 1

        if len(active_players()) > 1:
            finalists: list[PokerPlayer] = []
            for player in active_players()[:-1]:
                res = ask(player, table_cards)
                if res:
                    finalists.append(res)
            if not len(finalists):
                ...
                #DO player active_players()[-1] wins

            else:
                res = ask(active_players[-1], table_cards)
                if res:
                    finalists.append(res)
                best_hand = compare_combinations(
                    [poker_combination(player.cards, table_cards, game_type)
                        for player in finalists])
                finalists = {
                    player : poker_combination(player.cards, table_cards, game_type)
                        for player in finalists
                        if poker_combination(player.cards, table_cards, game_type).hand == best_hand.hand
                }

                ...

            ...

        ...
        #TODO:

    def game(self, game_type):
        small_blind = 10
        rounds = 0
        self.players[0].is_dealer = True
        #DO announce the start of the game
        while len([p for p in self.players if p.bankroll]) > 1:
            self.party(small_blind * 2**(rounds//5), game_type)
            rounds += 1
        #DO announce that the game finished and choose to either continue or exit

class MyPrimitiveEventQueue:
    class Lock:
        def __init__(self):
            self.lock = False

        def __enter__(self):
            while self.lock:
                continue
            self.lock = True

        def __exit__(self, *err_args):
            self.lock = False

    def __init__(self, dt = 1/350) -> None:
        self.dt = dt
        self.lock = self.Lock()
        self.queue: list[MyEvent] = []

    def __lock_control(func):
        def _(self: 'MyPrimitiveEventQueue', *args):
            t.sleep(self.dt)
            with self.lock:
                return func(self, *args)
        return _

    @__lock_control
    def push(self, event: 'MyEvent'):
        self.queue.append(event)

    @__lock_control
    def get(self, tag=None):
        '''Return None if no value with tag was found'''

        if not len(self.queue):
            return
        if tag == None:
            return self.queue.pop(0)

        for i, elem in enumerate(self.queue):
            if elem.tag == tag:
                return self.queue.pop(i)[1]

class MyEvent:
    # Codes: 0 - Player, 1 - Server
    # Player - conn - action (+args)
    # Player - conn - chat message
    # Player - conn - disconnect
    # Server - text message
    # Server - game finished
    # Server - game continues
    # Actions:
    codes = {
        "Shutdown"          : -5,                               # server
        "Timeout"           : -2,                               # player
        "Disconnect"        : -1,                               # player
        "Act"               : 0,                                # player ...
            "Check"         : 1,
            "Call"          : 2,                                    # argument - sum
            "Bet"           : 3,                                    # argument - sum
            "Raise"         : 4,
            "Fold"          : 5,
            "Quit"          : 6,
            "Muck"          : 7,
            "Show"          : 8,
        "Chat message"      : 10                                # player
    }

    def __init__(self, code, name, args: tuple = None):
        self.code = code
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}, code={self.code}, name={self.name}, args={self.args}>'
