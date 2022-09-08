import tkinter as tk
import tkinter.font as tkf
from consts import *

class Sprite:
    cache = []
    def __new__(cls, master: 'Window', file: str):
        instance = tk.PhotoImage(master=master.win, file=file)
        cls.cache.append(instance)
        return instance

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
