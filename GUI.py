import tkinter as tk
import tkinter.font as tkf
from consts import *
from game import *

class Sprite:
    cache = []
    def __new__(cls, master: 'Window', file: str):
        instance = tk.PhotoImage(master=master.win, file=file)
        cls.cache.append(instance)
        return instance

class WindowSheet:
    def __init__(self, master: 'Window',
                 grid_items: list[tk.Widget] = None,
                 place_items: list[tk.Widget] = None
                 ):
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
