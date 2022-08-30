import typing as T

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
    font_game_names = 'Helvetica', '10', 'bold'

# other consts
SUITS = SPADE, HEART, CLUB, DIAMOND = '♠♥♣♦'
ORDER = [*range(2, 11), *'JQKA'] # 2 3 ... 10 J K Q A
DECK = [(index, suit) for suit in SUITS for index in ORDER]

GameCodeType = int
GCODE_SUCCESS = 0
GCODE_DISCONNECT = 1
GCODE_SHUT_CONNECTION = -1
GCODE_SERVER_FULL = 2

CNF_MENU_BUTTON = {'font' : Params.font_head, 'bg' : 'DeepSkyBlue3', 'activebackground' : 'DeepSkyBlue2'}
CNF_LABEL = {'bg' : Params.color_BG, 'fg' : 'white'}
CNF_LABEL_G = {'rowspan' : 4, 'sticky' : 'NEWS'}
CNF_IMG_G = {'sticky' : 'NEWS'}
CNF_GAME_BUTTON_G = {'rowspan' : 6, 'columnspan' : 9, 'sticky' : 'NEWS'}

ACTIONS_CHECK = 'Check'
ACTIONS_BET = 'Bet'
ACTIONS_RAISE = 'Raise'
ACTIONS_CALL = 'Call'
ACTIONS_FOLD = 'Fold'
ACTIONS_SHOW = 'Show'
ACTIONS_MUCK = 'Muck'
ACTIONS_QUIT = 'Quit'

CardRank = T.Union[int, str]
CardSuit = str
CardValue = tuple[CardRank, CardSuit]

DIR = '\\'.join(__file__.split('\\')[:-1])
TITLE = "Tony\'s Card Games Catalogue"