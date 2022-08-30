# socket consts
HEADLEN = 8
SOCKET_TIMEOUT = 3

# other consts
SPADE, HEART, CLUB, DIAMOND = '♠♥♣♦'
SUITS = [SPADE, HEART, CLUB, DIAMOND]
ORDER = [*range(2, 11), *'JQKA'] # 2 3 ... 10 J K Q A
DECK = [(index, suit) for suit in SUITS for index in ORDER]

class EventPrivacyType:
    ALL = "All"
    GAME = "Game"
    PERSONAL = "Personal"
    NONGAME = "Non-Game"

ACTIONS_CHECK = 'Check'
ACTIONS_BET = 'Bet'
ACTIONS_RAISE = 'Raise'
ACTIONS_CALL = 'Call'
ACTIONS_FOLD = 'Fold'
ACTIONS_SHOW = 'Show'
ACTIONS_MUCK = 'Muck'
ACTIONS_QUIT = 'Quit'

def check_ip_mask(ip: str):
    ip = ip.split('.')
    return not ((len(ip) != 4) or any(not (arg.isdigit() and not (arg.startswith('0') and len(arg) > 1) and 0 <= int(arg) < 256) for arg in ip))

class Trigger:
    instances: list['Trigger'] = []

    def __init__(self, state = False) -> None:
        self.state = state
        Trigger.instances += [self]

    def __bool__(self) -> bool:
        return bool(self.state)

    def __repr__(self) -> str: # just in case
        return f'<BoolTrigger, state={self.state}>'

    def toggle(self): self.state = not self.state

    @classmethod
    def disable(cls):
        '''Put all instances' states to 1'''
        for i in cls.instances:
            i.state = True

class GameCode:
    def __init__(self, ind: int, message: str = None) -> None:
        self.ind, self.message = ind, message

    def __eq__(self, target: 'GameCode'):
        return isinstance(target, GameCode) and self.ind == target.ind

    def __len__(self):
        return 1 # for message length check in main

    def __repr__(self):
        return f'<GameCode, code={self.ind}, message={self.message}>'

class PokerCombination:
    name: str
    hand = [0]
    kicker: list[int] = None
    def __eq__(self, __o: 'PokerCombination'):
        return self.hand == __o.hand and self.kicker == __o.kicker

class Params:
    color_white = '#fff'
    color_light_grey = '#e0f0e0'
    color_grey = '#aaa'
    color_warning = '#fe1'
    color_BG = '#484'
    color_BG_game = '#1045a0'
    color_black = '#000922'
    color_dark_blue = '#002030'
    color_gold = '#ff3'

    font_head, font_middle, font_low = (('Century Gothic', str(p), 'bold') for p in [14, 12, 11])
    font_players = 'Helvetica', '12', 'bold'
    font_chat = 'Helvetica', '10', 'bold'

CODE_SUCCESS = GameCode(700)
CODE_DISCONNECT = GameCode(712)
CODE_SHUT_CONN = GameCode(711, 'Connection closed by host')
CODE_SERVER_FULL = GameCode(731, 'Lobby is full')

CNF_MENU_BUTTON = {'font' : Params.font_head, 'bg' : 'DeepSkyBlue3', 'activebackground' : 'DeepSkyBlue2'}
CNF_LABEL = {'bg' : Params.color_BG, 'fg' : 'white'}
CNF_LABEL_G = {'rowspan' : 4, 'sticky' : 'NEWS'}
CNF_IMG_G = {'sticky' : 'NEWS'}
CNF_GAME_BUTTON_G = {'rowspan' : 6, 'columnspan' : 9, 'sticky' : 'NEWS'}

__all__ = [
    # constants
    'HEADLEN',

    'CODE_SHUT_CONN',
    'CODE_SUCCESS',
    'CODE_DISCONNECT',
    'CODE_SERVER_FULL',

    'ACTIONS_CHECK',
    'ACTIONS_BET',
    'ACTIONS_RAISE',
    'ACTIONS_CALL',
    'ACTIONS_FOLD',
    'ACTIONS_SHOW',
    'ACTIONS_MUCK',
    'ACTIONS_QUIT',

    'SUITS',
    'SPADE',
    'HEART',
    'CLUB',
    'DIAMOND',
    'ORDER',
    'DECK',

    'CNF_MENU_BUTTON',
    'CNF_LABEL',
    'CNF_LABEL_G',
    'CNF_IMG_G',
    'CNF_GAME_BUTTON_G',

    'SOCKET_TIMEOUT',

    # functions
    'check_ip_mask',

    # classes
    'EventPrivacyType',
    'Trigger',
    'GameCode',
    'PokerCombination',
    'Params',
]

