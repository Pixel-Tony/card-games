# Constants section
import enum
import random
import os.path
import socket
import pickle
import typing as T
import tkinter as tk
import tkinter.font as tkf
import itertools as iterts
import threading as thr
import time as t
import select as sel
from urllib import request as urlreq
from urllib.error import URLError


class Colors(str, enum.Enum):
    WHITE = '#fff'
    LGREY = '#e0f0e0'
    GREY = '#aaa'
    WARNING = '#fe1'
    BG = '#484'
    BG_GAME = '#1045a0'
    PITCH_BLACK = '#000922'
    DBLUE = '#002030'
    GOLD = '#ff3'

class Fonts(tuple, enum.Enum):
    HEAD = 'Century Gothic', '14', 'bold'
    MIDDLE = 'Century Gothic', '12', 'bold'
    LOW = 'Century Gothic', '11', 'bold'
    PLAYER_TABLE = 'Helvetica', '12', 'bold'
    CHAT = 'Helvetica', '10', 'bold'
    GAME_NAMES = 'Helvetica', '10', 'bold'

SUITS = SPADE, HEART, CLUB, DIAMOND = '♠♥♣♦'
ORDER = [*range(2, 11), *'JQKA']  # 2 3 ... 10 J K Q A
DECK = [(index, suit) for suit in SUITS for index in ORDER]

GC_SUCCESS = 0
GC_FAIL = 1
GC_ERR_LOBBY_FULL = 10
GC_ERR_LOBBY_CLOSING = 11
GC_ERR_CONN_BROKE = 20
GC_EVENT = 2
GC_DISCONNECT = 6

CNF_MENU_BUTTON = {
    'font': Fonts.HEAD,
    'bg': 'DeepSkyBlue3',
    'activebackground': 'DeepSkyBlue2'
}
CNF_LABEL = {'bg': Colors.BG, 'fg': 'white'}
CNF_ENTRY = {'font' : Fonts.MIDDLE, 'bg' : 'CadetBlue1'}

B_STATES = ['disabled', 'normal']

class PokerActionType(enum.Enum):
    CHECK = 'Check'
    BET = 'Bet'
    RAISE = 'Raise'
    CALL = 'Call'
    FOLD = 'Fold'
    SHOW = 'Show'
    MUCK = 'Muck'
    QUIT = 'Quit'

CardRank = T.Union[int, str]
CardSuit = str
CardValue = tuple[CardRank, CardSuit]
Socket = socket.socket

TITLE = "Tony\'s Card Games Catalogue"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# App functionality section
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class PlayerData:
    data: dict

    @classmethod
    def load(cls) -> dict:
        # if os.path.exists('./data/player.txt'):
        #     lines = open('./data/player.txt', 'r').readlines()
        #     cls.data = {'Name' : lines[0], 'IP' : lines[1]}
        # else:
            cls.data = {'Name' : '', 'IP' : ''}
            return cls.data

    @classmethod
    def write(cls):
        with open('./data/player.txt', 'w') as file:
            file.writelines(cls.data.values())

    def __new__(cls): return cls.data

class TimedAction:
    def __new__(cls, func, dt: float, args = (), kwgs = {}):
        t1 = t.perf_counter_ns()
        val = func(*args, **kwgs)
        if left := (dt - (t.perf_counter_ns() - t1) * 1e9) > 0:
            print(left)
            t.sleep(left)
        return val

def wait_until_dt(dt: float):
    def _(func, *args, **kwgs):
        t1 = t.perf_counter_ns()
        func(*args, **kwgs)
        if (d:= t.perf_counter_ns() - t1) < dt:
            t.sleep(d * 1e9)
    return lambda func: lambda *args, **kwgs: _(func, *args, **kwgs)

class Trigger:
    def __init__(self, state = False): self.state = bool(state)
    def __bool__(self): return self.state
    def __repr__(self): return f'<BoolTrigger, state={self.state}>'
    def toggle(self): self.state = not self.state

class PokerHand:
    name: str
    hand = [0]
    kicker: list[int] = None
    def __eq__(self, other: 'PokerHand'):
        return self.hand == other.hand and self.kicker == other.kicker

    def __str__(self): return self.name

class Poker:
    @staticmethod
    def deal_cards(p_num: int, omaha: bool):
        return [random.choice(DECK) for i in range(p_num*(2 + 2*omaha) + 5)]

    @staticmethod
    def create_hand(cards: T.Iterable[CardValue]):
        '''Return the best possible Texas Hold'em Poker hand of available with input cards\n```
        | 10 - Flush Royale | 9 - Straight flush
        | 8 - Four          | 7 - Full House
        | 6 - Flush         | 5 - Straight
        | 4 - Set           | 3 - Two pairs
        | 2 - Pair          | 1 - Higher card
        '''
        def order_range(start, stop):
            return [ORDER[i] for i in range(start, stop)]
        # assert len(cards) == 5, "list length is not 5"
        cards = sorted(cards, key=lambda card: ORDER.index(card[0]), reverse=1)

        nominals: list
        suits: list
        nominals, suits = zip(*cards)
        nominal_quantts = {el : nominals.count(el) for el in set(nominals)}
        suit_quantts = {el : suits.count(el) for el in set(suits)}
        comb = PokerHand()

        if any(suit_quantts[x] >= 5 for x in suit_quantts):     # 10 - 9 - 6
            suit = [*filter(lambda a: suit_quantts[a] >= 5, suit_quantts)][0]
            card_noms = [*zip(*filter(lambda c: c[1] == suit, cards))][0]

            for i in range(len(ORDER) - 5, -2, -1):             # 10 - 9
                if (set(order_range(i, i + 5)).issubset(card_noms)): #lst in lst
                    if i == len(ORDER) - 5:                     # 10
                        comb.name = f'Flush Royale: A to 10 of {suit}'
                        comb.hand = [10]
                    else:                                       # 9
                        comb.name = f'Straight Flush: {ORDER[i + 4]} to {ORDER[i]} of {suit}'
                        comb.hand = [9, i + 4]
                    return comb
                                                                # 6
            comb.name = f"Flush: {'-'.join(map(str, card_noms))} of {suit}"
            comb.hand = [6] + [ORDER.index(el) for el in card_noms[:5]]

        if 4 in nominal_quantts.values():                       # 8
            main_nominal = [a for a, y in nominal_quantts.items() if y == 4][0]
            comb.name = f'Four of {main_nominal}\'s'
            comb.hand = [8, ORDER.index(main_nominal)]
            comb.kicker = [ORDER.index(a) for a in nominals[4:]][:1]
            return comb

        if 3 in nominal_quantts.values() and comb.hand[0] <= 4: # 7 - 4
            set_nominals = [x for x, y in nominal_quantts.items() if y == 3]
            set_nominals.sort(key=ORDER.index)
            pair_nominals = [x for x, y in nominal_quantts.items() if y == 2]
            pair_nominals.sort(key=ORDER.index)

            if len(set_nominals) > 1:                           # 7
                main_nominal = set_nominals[-1]
                pair_nominal = max([*pair_nominals, set_nominals[-2]],
                                        key=ORDER.index)
                comb.name = f'Full House: set of {main_nominal} and a pair of {pair_nominal}'
                comb.hand = [7, *map(ORDER.index, (main_nominal, pair_nominal))]
                return comb

            comb.name = f'Set of {set_nominals[0]}'             #4
            comb.hand = [4, ORDER.index(set_nominals[0])]
            comb.kicker = [ORDER.index(a) for a in nominals if a != set_nominals[0]][:2]

        for i in range(len(ORDER) - 5, -2, -1): # 5
            if all(order_range(i, i + 5)[::-1][n] in nominals for n in range(5)):
                comb.name = f'Straight: {ORDER[i + 4]} to {ORDER[i]}'
                comb.hand = [5, i + 4]
                return comb

        if 2 in nominal_quantts.values() and comb.hand[0] < 1:  #3 - 2
            pair_nominals = [x for x, y in nominal_quantts.items() if y == 2]
            pair_nominals.sort(key=ORDER.index)

            if len(pair_nominals) > 1:
                comb.name = f'Two pairs: a pair of {pair_nominals[-1]} and a pair of {pair_nominals[-2]}'
                comb.hand = [3] + [ORDER.index(a) for a in pair_nominals[-2:][::-1]]
                comb.kicker = [ORDER.index(a) for a in nominals if a not in pair_nominals[-2:]][:1]
            else:
                comb.name = f'Pair of {pair_nominals[0]}'
                comb.hand = [2] + [ORDER.index(pair_nominals[0])]
                comb.kicker = [ORDER.index(a) for a in nominals if a != pair_nominals[0]][:3]
            return comb

        if comb.hand[0] == 0:
            comb.name = f'Higher card: {nominals[0]}'
            _noms = [ORDER.index(card) for card in nominals[1:]][:5]
            comb.hand = [1, _noms[0]]
            comb.kicker = [_noms[1:]]

        return comb

    @staticmethod
    def best_poker_hand(*hands: PokerHand):
        '''Return best combination of `combinations`'''
        best = hands[0]
        for comb in hands[1:]:
            if comb.hand > best.hand:
                best = comb
            elif comb.hand == best.hand and \
                not comb.kicker or comb.kicker > best.kicker:
                    best = comb
        return best

    @staticmethod
    def best_hand(player_cards: list['CardValue'],
                  table_cards: list['CardValue'],
                  omaha: bool
                  ):
        if not omaha:
            return Poker.create_hand(player_cards + table_cards)

        p_card_vars = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        if not table_cards:
            return Poker.best_poker_hand([
                Poker.create_hand([player_cards[i] for i in p_var])
                    for p_var in p_card_vars
            ])

        table_card_variants = iterts.combinations(range(len(table_cards)), 3)
        return Poker.best_poker_hand([
            Poker.create_hand([player_cards[i] for i in p_var]
                + [table_cards[j] for j in t_var])
                    for p_var in p_card_vars
                        for t_var in table_card_variants
        ])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# GUI section
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Sprite:
    __cache = set()
    def __new__(cls, master: 'GUIWindow', path: str):
        instance = tk.PhotoImage(master=master.win, file=path)
        cls.__cache.add(instance)
        return instance

    def __del__(self):
        self.__class__.__cache.pop(self)

class GUIModernEntry(tk.Entry):
    def __new__(cls, *args, **kwgs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwgs)
        return cls.smart(instance)
        return cls.smart(super().__new__(*args, **kwgs))

    @classmethod
    def smart(cls, entry: tk.Entry):
        entry.bind(f'<Control-Key>', cls.modern_handler)
        return entry

    @classmethod
    def modern_handler(cls, ev: tk.Event):
        keybinds = {
            67: cls.modern_kb_copy,
            86: cls.modern_kb_paste,
            88: cls.modern_kb_cut,
            65: cls.modern_kb_select_all
        }
        if ev.keycode in keybinds:
            keybinds[ev.keycode](ev.widget)

    @staticmethod
    def modern_kb_select_all(entry: tk.Entry):
        entry.select_range(0, tk.END)

    @staticmethod
    def modern_kb_cut(entry: tk.Entry):
        if not entry.select_present(): return
        start = entry.index(tk.SEL_FIRST)
        end = entry.index(tk.SEL_LAST)
        entry.clipboard_append(entry.get()[start:end])
        entry.delete(start, end)

    @staticmethod
    def modern_kb_paste(entry: tk.Entry):
        if entry.select_present():
            start = entry.index(tk.SEL_FIRST)
            end = entry.index(tk.SEL_LAST)
        else:
            start = end = entry.index(tk.INSERT)
        entry.delete(start, end)

        try:
            entry.insert(start, entry.master.clipboard_get())
        except tk.TclError:
            entry.insert(start, '')

    @staticmethod
    def modern_kb_copy(entry: tk.Entry):
        if not entry.select_present():
            entry.clipboard_clear()
            entry.clipboard_append(entry.selection_get())

class GUIWindowLayer:
    def __init__(self, master: 'GUIWindow', items: list[tk.Widget] = ...):
        self.collection: dict[tk.Widget, dict[str, tk._PlaceInfo]] = {}
        if items != ...:
            self.add(items)
        master.layers += [self]

    def add(self, items: list[tk.Widget]):
        for item in items:
            self.collection[item] = item.place_info()

    def hide(self):
        [wg.place_forget() for wg in self.collection]

    def show(self):
        [wg.place(**p_info) for wg, p_info in self.collection.items()]

class GUIWindow:
    current: "GUIWindow" = None
    did_quit = False
    _instances: list["GUIWindow"] = []
    _initiated: tk.Tk | tk.Toplevel = ...

    def __init__(self, size: tuple, title: str, bg: str = ...):
        self.layers: list[GUIWindowLayer] = []
        if GUIWindow._initiated == ...:
            GUIWindow._initiated = self.win = tk.Tk()
        else:
            self.win = tk.Toplevel(GUIWindow._initiated)
        self.win.protocol("WM_DELETE_WINDOW", GUIWindow.destroy)
        self.win.resizable(0, 0)
        self.win.title(title)
        if bg != ...:
            self.win['bg'] = bg
        self.hidden: bool = True

        a = (self.win.winfo_screenwidth() - size[0]) // 2
        b = (self.win.winfo_screenheight() - size[1]) // 2
        self.geometry = f'{size[0]}x{size[1]}+{a}+{b}'
        self.win.geometry(self.geometry)
        self.layer = None
        GUIWindow.current = self

    def hide(self):
        self.win.withdraw()
        self.hidden = True

    def show(self, layer: GUIWindowLayer, center_after: bool = False):
        if center_after:
            self.win.geometry(self.geometry)

        self.hidden = False
        [lyr.hide() for lyr in self.layers if lyr != layer]
        layer.show()
        self.layer = layer
        self.win.deiconify()
        self.win.focus_set()
        GUIWindow.current = self

    def mainloop(self): self.win.mainloop()
    def update(self): self.win.update()

    @staticmethod
    def destroy():
        GUIWindow.did_quit = True
        GUIWindow._initiated.destroy()

    @staticmethod
    def switch_to(to: 'GUIWindow', which: GUIWindowLayer):
        if (GUIWindow.current is not which):
            GUIWindow.current.hide()
        to.show(which)

class GUIChat:
    def __init__(self, pad_coords: tuple[int, int], canv: tk.Canvas, font):
        self.canv = canv
        self.x, self.y = pad_coords
        self.font = tkf.Font(self.canv, font)
        self.line_limit = int(canv['scrollregion'].split(' ')[2]) - self.x
        self.colors = {}

    def set_colors(self, *, author = ..., msg = ..., sysmsg = ...):
        if author != ...: self.colors['a'] = author
        if msg != ...: self.colors['m'] = msg
        if sysmsg != ...: self.colors['s'] = sysmsg

    def post(self, message: list[tuple]):
        def add_string(s: str, color: str = None):
            nonlocal x, y
            for char in s:
                w = self.font.measure(char)
                if w + x + 1 > self.line_limit or char == '\n':
                    x = self.x
                    y += CHAR_H_WITH_BUFF
                    if char == '\n':
                        continue
                self.canv.create_text(
                    x, y, text=char, anchor='nw', justify='left',
                    font = self.font, fill=color)
                x += w

        CHAR_H_WITH_BUFF = 22
        x, y = self.x, self.y

        while message:
            author, text = message.pop(0)
            if author == None:
                add_string(text, self.colors['s'])
            else:
                add_string(author + ': ', self.colors['a'])
                add_string(text, self.colors['m'])
            if message:
                add_string('\n')

        self.y = y + CHAR_H_WITH_BUFF
        scrollregion = [*map(int, self.canv['scrollregion'].split(' '))]
        while scrollregion[3] - self.y < CHAR_H_WITH_BUFF:
            scrollregion[3] += CHAR_H_WITH_BUFF

        self.canv.configure(scrollregion=scrollregion)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Networking and stuff
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Network:
    @staticmethod
    def _deco_ret_on_fail(func):
        def _(*args):
            try:
                return func(*args)
            except Exception as e:
                return args
        return _

    @staticmethod
    def ip_get() -> str:
        try:
            ip = urlreq.urlopen("https://ident.me", timeout=1.5
            ).read().decode("utf8")
        except URLError:
            ip = socket.gethostbyname(socket.gethostname())
        return ip

    @staticmethod
    @_deco_ret_on_fail
    def receive(sock_where: Socket):
        '''Receive an object from `sock_where`'''
        objlen = sock_where.recv(8).decode()
        if not objlen:
            return None
        objlen = int(objlen)
        res = b''
        while len(res) < objlen:
            res += sock_where.recv(min(2048, objlen - len(res)))
        return pickle.loads(res)

    @staticmethod
    def send(sock_where: Socket, obj):
        '''Send object `obj` to `sock_where`'''
        obj = pickle.dumps(obj)
        obj = str(len(obj)).zfill(8).encode() + obj
        try:
            return sock_where.sendall(obj) is None
        except Exception:
            return False

    @staticmethod
    def validate_ip(ip: str):
        ip = ip.split('.')
        if len(ip) != 4:
            return False

        for arg in ip:
            # if not numeric or is starting with '0' while != 0
            if not arg.isdigit() or (arg.startswith('0') and len(arg) > 1) \
                    or 0 > int(arg) >= 256:
                return False
        return True

class PokerServer:
    def __init__(self, port: int):
        self.sock = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen(9)
        self.conns = {
            self.sock : {
                'Name' : PlayerData()['Name'], 'ID' : 0, 'Pending' : False
            }
        }
        self.readers, self.listeners = [self.sock], []

    def start(self, tr_started: Trigger, tr_cancelled: Trigger):
        def _upd():
            lst_read, lst_send, _ = sel.select(
                self.readers, self.listeners, [])
            for conn in lst_read: ...
            for conn in lst_send: ...
            print('Thread alive')

        def inner(t_started: Trigger, t_cancelled: Trigger):
            while not (t_started or t_cancelled):
                TimedAction(_upd, 1/60)
            print('Thread dies')

        self.tr_started = tr_started
        self.tr_cancelled = tr_cancelled
        self.worker = thr.Thread(
            target=inner,
            args=(self.tr_started, self.tr_cancelled)
            )
        self.worker.start()