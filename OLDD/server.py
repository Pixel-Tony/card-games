from socket import (socket as Socket,
                    gethostbyname as sock_gethostbyname,
                    gethostname as sock_gethostname,
                    SOCK_STREAM as socket_SOCK_STREAM,
                    AF_INET as socket_AF_INET)
from urllib import request as urlreq
from urllib.error import URLError
import pickle
from consts import *
from typing import Union

def deco_ret_arg_on_error(return_arg=False):
    def wrap(func):
        def _(*args):
            try:
                return func(*args)
            except Exception as e:
                return args if return_arg else e
        return _
    return wrap

def get_ip() -> str:
    try:
        ip = urlreq.urlopen(
            "https://ident.me", timeout=1.5
        ).read().decode("utf8")
    except URLError:
        ip = sock_gethostbyname(sock_gethostname())
    return ip

deco_ret_arg_on_error(True)
def recvobj(sock_where: Socket):
    '''Receive an object from `sock_where`'''
    objlen = sock_where.recv(8).decode()
    if not objlen:
        return None
    objlen = int(objlen)
    res = b''
    while len(res) < objlen:
        res += sock_where.recv(min(2048, objlen - len(res)))
    return pickle.loads(res)

@deco_ret_arg_on_error(True)
def sendobj(sock_where: Socket, obj) -> Union[None, Socket]:
    '''Send object `obj` to `sock_where`\n\nreturn None on success'''
    # print('sent', obj)
    obj = pickle.dumps(obj)
    obj = str(len(obj)).zfill(8).encode() + obj
    return sock_where.sendall(obj)

IP, PORT = get_ip(), 50240

def check_ip_mask(ip: str):
    ip = ip.split('.')
    if len(ip) != 4:
        return False

    for arg in ip:
        # if not numeric or is starting with '0' while not being equal to 0
        if not arg.isdigit() or (arg.startswith('0') and len(arg) > 1):
            return False
        elif 0 > int(arg) >= 256:
            return False
    return True

def sendobj_ext(sock_where: Socket, obj, proto_failure):
    if sendobj(sock_where, obj):
        proto_failure()

def recvobj_ext(sock_where: Socket, proto_failure):
    result = recvobj(sock_where)
    if isinstance(result, Socket):
        proto_failure()

    return result


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


# class ____ServerPokerTable:
#     def __init__(self, players: list[PokerPlayer]):
#         self.players = players

#     def _set_default(self): [p.set_default() for p in self.players]

#     def _alive_players(self):
#         return [p for p in self.players if p.bankroll and not p.folded]

#     def wait_for_game_event(self):
#         pass


#     def _party(self, small_blind: int, is_omaha: bool):
#         def share_the_pot(pot: int, *winners: PokerPlayer):
#             for p in winners:
#                 p.bankroll += pot // len(winners)

#         def get_options(p: PokerPlayer, bet=0) -> list[str]:
#             if not p.bankroll or p.folded:
#                 return

#             options = []
#             if bet <= p.current_bet:
#                 options.append(ACTIONS_CHECK)
#             else:
#                 options.append(ACTIONS_CALL)

#             if bet == 0:
#                 options.append(ACTIONS_BET)
#             elif p.bankroll > bet*2:
#                 options.append(ACTIONS_RAISE)

#             options.extend((ACTIONS_FOLD, ACTIONS_QUIT))

#             return options

#         def p_action(p: PokerPlayer, action: str):
#             pass

#         def active_players():
#             return [p for p in self.players if not p.folded]

#         def showdown_ask(p: PokerPlayer):
#             '''send cards, send two options, get result'''
