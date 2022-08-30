import random
import tkinter as tk
import tkinter.font as tkf
from itertools import combinations as itertools_combs
import time as t
import os.path
from consts import *

###########################################################################
# # # # # # # # # # # # # #| Generic utilities |# # # # # # # # # # # # # #
###########################################################################
def load_player_data() -> dict[str, str]:
    if os.path.exists('./data/player.json'):
        lines = open('./data/player.json', 'r').readlines()
        return {'name' : lines[0], 'IP' : lines[1]}
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
                      game_type: T.Literal[0, 1]):
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

