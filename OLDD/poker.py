import random
import tkinter as tk
import tkinter.font as tkf
from consts import *
from itertools import combinations as itertools_combs
import time as t
import os.path
import json

###########################################################################
# # # # # # # # # # # # # #| Generic utilities |# # # # # # # # # # # # # #
###########################################################################
def general_get_player_info() -> dict[Literal['name', 'IP'], str]:
    if os.path.exists('./data/player.json'):
        return json.load(open('./util/player.json'), 'r')
    return {'name' : '', 'IP' : ''}

def delta_time(dt: float):
    def _(func):
        def _2(*args, **kwargs):
            t1 = t.perf_counter()
            result = func(*args, **kwargs)
            t2 = t.perf_counter()
            if t2 - t1 < dt:
                t.sleep(dt - (t1 - t2))
            return result
        return _2
    return _

class Trigger:
    instances: list['Trigger'] = []

    def __init__(self, state = False) -> None:
        self.state = state
        Trigger.instances += [self]

    def __bool__(self) -> bool:
        return bool(self.state)

    def __repr__(self) -> str:
        return f'<BoolTrigger, state={self.state}>'

    def toggle(self): self.state = not self.state

    @classmethod
    def disable(cls):
        '''Put all instances' states to 1'''
        for i in cls.instances:
            i.state = True

class PokerCombination:
    name: str
    hand = [0]
    kicker: list[int] = None
    def __eq__(self, __o: 'PokerCombination'):
        return self.hand == __o.hand and self.kicker == __o.kicker

    def __str__(self) -> str:
        return self.name

def poker_deal_cards(player_count: int, game_type: int):
    return [random.choice(DECK)
        for i in range((player_count*(2 + 2*game_type)) + 5)]

def poker_holdem_combination(cards: list['CardValue']):
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
    comb = PokerCombination()

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

def poker_compare_combinations(combinations: list[PokerCombination]):
    '''Return best combination of `combinations`'''
    current = combinations[0]
    for comb in combinations[1:]:
        if comb.hand > current.hand:
            current = comb
        elif comb.hand == current.hand:
            if not comb.kicker or comb.kicker > current.kicker:
                current = comb

    return current

def poker_combination(player_cards: list['CardValue'],
                      table_cards: list['CardValue'],
                      game_type: Literal[0, 1]):
    if game_type == 0:
        return poker_holdem_combination(player_cards + table_cards)

    player_card_variants = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    if not len(table_cards):
        return poker_compare_combinations(
                [poker_holdem_combination([player_cards[i] for i in p_var]
            ) for p_var in player_card_variants])
    result = []
    table_card_variants = [*itertools_combs(range(len(table_cards)), 3)]
    for p_var in player_card_variants:
        for t_var in table_card_variants:
            result.append(poker_holdem_combination(
                [player_cards[i] for i in p_var]
                + [table_cards[j] for j in t_var]
            ))
    return poker_compare_combinations(result)

def entry_smartify(entry: tk.Entry):
    def copy(entry: tk.Entry):
        if entry.select_present():
            entry.clipboard_clear()
            entry.clipboard_append(entry.selection_get())

    def paste(entry: tk.Entry):
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

    def cut(entry: tk.Entry):
        if not entry.select_present(): return
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

    def keyhandler(ev: tk.Event):
        if ev.keycode in keybinds:
            keybinds[ev.keycode](ev.widget)

    entry.bind(f'<Control-Key>', keyhandler)
    return entry

###########################################################################
# # # # # # # # # # # # # # # #| GUI group |# # # # # # # # # # # # # # # #
###########################################################################
class Sprite:
    cache = []
    def __new__(cls, master: 'Window', file):
        instance = tk.PhotoImage(master=master.win, file=file)
        cls.cache.append(instance)
        return instance

class WindowSheet:
    def __init__(self, master: 'Window',
                 grid_items: list[tk.Widget] = None,
                 place_items: list[tk.Widget] = None):
        self.grid_collection: list[tk.Widget] = []
        self.place_collection: dict[tk.Widget, dict[str, tk._PlaceInfo]] = {}

        if place_items:
            self.add_place(*place_items)

        if grid_items:
            self.add_grid(*grid_items)

        master.sheets.append(self)

    def add_place(self, *items: tk.Widget):
        for item in items:
            self.place_collection[item] = item.place_info()

    def add_grid(self, *items: tk.Widget):
        self.grid_collection.extend(items)

    def hide(self):
        [*map(tk.Widget.grid_remove, self.grid_collection)]
        [*map(tk.Widget.place_forget, self.place_collection.keys())]

    def show(self):
        [widget.grid() for widget in self.grid_collection]
        [widget.place(**info)
            for widget, info in self.place_collection.items()]

class Window:
    __current_window: 'Window' = None
    __instances: list['Window'] = []
    did_quit = False

    def __init__(self,
                 size: tuple[int, int],
                 title: str,
                 master: 'Window' = ...,
                 bg: str = ...) -> None:
        self.sheets: list[WindowSheet] = []
        self.win = tk.Tk() if master == ... else tk.Toplevel(master.win)
        self.win.protocol("WM_DELETE_WINDOW", Window.main_quit)
        self.win.resizable(0, 0)
        self.win.title(title)
        if bg != ...:
            self.win['bg'] = bg
        self.is_hidden: bool = False

        a = (self.win.winfo_screenwidth() - size[0]) // 2
        b = (self.win.winfo_screenheight() - size[1]) // 2
        self.geometry = f'{size[0]}x{size[1]}+{a}+{b}'
        self.win.geometry(self.geometry)
        self.current_sheet = None

        for column in range(size[0] // 10):
            self.win.columnconfigure(column, weight=1, minsize=10)
        for row in range(size[1] // 10):
            self.win.rowconfigure(row, weight=1, minsize=10)

        if master == ...:
            Window.__instances.append(self)

        self.hide()

    def _show_sheet(self, sheet: WindowSheet):
        [sh.hide() for sh in self.sheets if sh != sheet]
        sheet.show()

    def hide(self):
        self.win.withdraw()
        self.is_hidden = True

    def show(self, sheet: WindowSheet):
        if self.is_hidden:
            # self.win.geometry(self.geometry) TODO: ?
            self.is_hidden = False

        self._show_sheet(sheet)
        self.current_sheet = sheet
        self.win.deiconify()
        self.win.focus_set()
        Window.__current_window = self

    @staticmethod
    def current():
        return Window.__current_window

    def mainloop_start(self):
        self.win.mainloop()

    def update(self):
        self.win.update()

    def x_enable_debug(self):
        column = lambda e: (e.x + (e.widget.winfo_x()
            if e.widget != self.win
                else 0))
        row = lambda e: (e.y + (e.widget.winfo_y()
            if e.widget != self.win
                else 0))
        self.win.bind('<Button-3>', lambda e: print(f'x (column): {column(e)}, y (row): {row(e)}'))

    @staticmethod
    def main_quit():
        Trigger.disable()
        for w in Window.__instances:
            w.win.destroy()
        Window.did_quit = True

    @staticmethod
    def switch(from_: 'Window', to: 'Window', which: int):
        from_.hide()
        to.show(which)

class ChatCanvas:
    LETTER_HEIGHT = 20

    def __init__(self, coords: tuple[int, int], canv: tk.Canvas, font, fill):
        self.canv = canv
        self.x, self.y = coords
        self.font = tkf.Font(self.canv, font)

        width = self.canv['scrollregion'].split(' ')[2]
        self.MAX_LINE_LEN = int(width) - self.x
        self.fill = fill

    def post_message(self, line: str):
        def add_char(char):
            nonlocal x, y
            if self.font.measure(char) + x + 1 > self.MAX_LINE_LEN:
                x = self.x
                y += self.LETTER_HEIGHT + 2

            self.canv.create_text(x, y, text=char, anchor='nw',
                                    justify='left', font=self.font,
                                    fill=color)
            x += self.font.measure(char) + 1

        colors = {
            'Blue'      : '#55F',
            'Red'       : '#F55',
            'Purple'    : '#608',
            'Yellow'    : '#FF1',
            'Green'     : '#1F1',
            ''          : self.fill
        }

        x, y = self.x, self.y
        color = self.fill

        while line:
            char, *line = line
            if char == '#':
                while char[-1] != '#' or len(char) == 1:
                    char += line[0]
                    line = line[1:]
                if char[1: -1].capitalize() in colors:
                    color = colors[char[1:-1]]
                else:
                    [add_char(ch) for ch in char.join('##')]
                continue
            add_char(char)

        self.y = y + self.LETTER_HEIGHT + 2
        scrollregion = [*map(int, self.canv['scrollregion'].split(' '))]
        while scrollregion[3] - self.y < self.LETTER_HEIGHT + 2:
            scrollregion[3] += self.LETTER_HEIGHT + 2

        self.canv.configure(scrollregion=scrollregion)

class CardSprite:
    def __init__(self, master: Window, value: CardValue, is_small=False):
        self.rank, self.suit = value
        self.master = master
        self.is_small = is_small

        file = './gfx/cards/' + str(DECK.index(value)) + '.png'
        self.label = tk.Label(master.win, image=Sprite(master, file))

        file_s = './gfx/cards/shirt.png'
        self.label_shirt = tk.Label(master.win, image=Sprite(master, file_s))

    def place(self, x: int, y: int, shirt_up=False):
        self.hide()
        if shirt_up and self.is_small:
            raise ValueError('Can\'t show shirt of the small card, dummy')
        width, height = [(80, 130), (64, 102)][self.is_small]
        (self.label, self.label_shirt)[shirt_up].place(
            x=x, y=y, height=height, width=width
        )

    def hide(self):
        self.label.place_forget()
        self.label_shirt.place_forget()

    def __repr__(self) -> str:
        return f'<CardSprite, {self.rank} of {self.suit}'

class PlayerGUI:
    __coords = {
        0 : {'cards': (216, 306), 'canvas': (20, 162), 'tokens': ((27, 28), (26, 28), (25, 29))},
        1 : {'cards': (436, 264), 'canvas': (320, 50), 'tokens': ((51, 28), (51, 27), (50, 27))},
        2 : {'cards': (616, 264), 'canvas': (620, 50), 'tokens': ((70, 27), (69, 27), (68, 27))},
        3 : {'cards': (818, 306), 'canvas': (920, 162), 'tokens': ((83, 28), (83, 29), (84, 29))},
        4 : {'cards': (813, 420), 'canvas': (920, 459), 'tokens': ((82, 50), (83, 50), (84, 49))},
        5 : {'cards': (616, 472), 'canvas': (620, 550), 'tokens': ((67, 50), (68, 50), (69, 51))},
        6 : {'cards': (436, 472), 'canvas': (320, 550), 'tokens': ((39, 51), (40, 51), (41, 51))},
        7 : {'cards': (216, 416), 'canvas': (20, 459), 'tokens': ((26, 49), (27, 49), (27, 50))}
    }

    def __init__(self, master: Window, sit: int, name: str):
        self.master = master
        self.sit = sit
        self.name = name
        self._bankroll = 0

        table_cards_file = ('./gfx/cards/cards'
                            + '_down'*(sit in {0, 4})
                            + '_up'*(sit in {3, 7})
                            + '.png')
        self.label_table_cards = tk.Label(
            master.win,
            image=Sprite(master, table_cards_file)
        )
        bg_color = '#666'
        self.frame = tk.Frame(master.win,
        bg=bg_color, highlightbackground='#dd6')
        self.label_name = tk.Label(self.frame,
                                   text=self.name,
                                   font=Params.font_game_names,
                                   background=bg_color,
                                   foreground='#fe2')
        self.label_bankroll = tk.Label(self.frame,
                                       font=Params.font_game_names,
                                       background=bg_color,
                                       foreground='#fb0')
        x, y = self.__coords[sit]['canvas']
        self.frame.place(x=x, y=y, width=161, height=130 + 21*2)
        self.label_name.place(x=2, y=2, bordermode='outside', width=161 - 4, height=21)
        self.label_bankroll.place(bordermode='outside', x=2, y=23, width=161 - 4, height=21)

        self.tokens: list[tk.Label] = []
        for color in {'blue', 'green', 'red'}:
            self.tokens.append(
                tk.Label(master.win,
                         image=Sprite(master, f'./gfx/tokens/{color}.png'))
            )

    def bind_card_sprite_pool(self,
                              pool: dict[CardValue, dict[str, CardSprite]]
                              ):
        self.deck_pool: dict[CardValue, dict[str, CardSprite]] = pool

    def real_cards_show(self,
                        cards: list[CardValue],
                        shirt_up: bool = False
                        ):
        x, y = self.__coords[self.sit]['canvas']
        y += 21*2
        dx = 81 // (len(cards) - 1)


        if hasattr(self, '_current_real_cards'):
            [self.deck_pool[card]['normal'].hide()
                for card in self._current_real_cards]

        self._current_real_cards = cards
        for i, card in enumerate(cards):
            self.deck_pool[card]['normal'].place(x + dx*i, y, shirt_up)

    def real_cards_hide(self):
        for card in self._current_real_cards:
            self.deck_pool[card]['normal'].hide()

    def bankroll_update(self, new_bankroll: int = ...):
        if new_bankroll != ...:
            self._bankroll = new_bankroll
        self.label_bankroll['text'] = str(self._bankroll) + '$'

    def tokens_update(self):
        n = sum(self._bankroll > a for a in {0, 330, 615})
        for i, token in enumerate(self.tokens[:n]):
            col, row = self.__coords[self.sit]['tokens'][i]
            token.grid(row=row, column=col, rowspan=1, columnspan=1)

    def table_cards_show(self):
        x, y = self.__coords[self.sit]['cards']
        w, h = ((66, 69) if self.sit in [3, 7] else             # diagonal /
                (71, 66) if self.sit in [0, 4] else             # diagonal \
                (48, 55))
        self.label_table_cards.place(x=x, y=y, width=w, height=h)

    def table_cards_hide(self):
        self.label_table_cards.place_forget()

    def frame_highlight(self, on=True):
        self.frame['highlightthickness'] = on * 2



class EventQueue:
    def __init__(self):
        self.queue = list()

    def add(self, event: dict):
        self.queue.append(event)

    def get(self) -> dict:
        if not len(self.queue):
            return None

        return self.queue.pop(0)

class PokerPlayer:
    def __init__(self, id: str, name: str, sit: int, start_bankroll: int):
        self.id = id
        self.name = name
        self.sit = sit

        self.current_bet = 0
        self.did_move = False
        self.is_dealer = False
        self.bankroll = start_bankroll
        self.set_default()

    def set_default(self):
        self.folded = False
        self.cards: list[CardValue] = []

    def do_bet(self, bet: int, *, small=False, big=False):
        self.current_bet = min(bet, self.bankroll)
        line = f'#Green#{self.name}##'
        if self.current_bet == self.bankroll:
            line += f" goes all-in (#Yellow#{self.current_bet}$##)"
        else:
            line += f" bets #Yellow#{self.current_bet}$##"

        if small or big:
            line += f" as a {['small', 'big'][big]} blind"

        return {'txt' : line, 'bet' : self.current_bet}

class ServerPokerHandler:
    def __init__(self, *players: PokerPlayer) -> None:
        self.players = list(players)


class ____ServerPokerTable:
    def __init__(self, players: list[PokerPlayer]):
        self.players = players

    def _set_default(self): [p.set_default() for p in self.players]

    def _alive_players(self):
        return [p for p in self.players if p.bankroll and not p.folded]

    def wait_for_game_event(self):
        pass


    def _party(self, small_blind: int, is_omaha: bool):
        def share_the_pot(pot: int, *winners: PokerPlayer):
            for p in winners:
                p.bankroll += pot // len(winners)

        def get_options(p: PokerPlayer, bet=0) -> list[str]:
            if not p.bankroll or p.folded:
                return

            options = []
            if bet <= p.current_bet:
                options.append(ACTIONS_CHECK)
            else:
                options.append(ACTIONS_CALL)

            if bet == 0:
                options.append(ACTIONS_BET)
            elif p.bankroll > bet*2:
                options.append(ACTIONS_RAISE)

            options.extend((ACTIONS_FOLD, ACTIONS_QUIT))

            return options

        def p_action(p: PokerPlayer, action: str):
            pass

        def active_players():
            return [p for p in self.players if not p.folded]

        def showdown_ask(p: PokerPlayer):
            '''send cards, send two options, get result'''
