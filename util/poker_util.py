from functools import reduce
from itertools import combinations as iter_combs
from random import randint
import socket

# Constants
SPADE, HEART, CLUB, DIAMOND = '♠','♥','♣','♦'
SUITS = [SPADE, HEART, CLUB, DIAMOND]
ORDER = [*range(2, 11), *'JQKA']
DECK = [(index, suit) for suit in SUITS for index in ORDER]

# Poker stuff
def add_to(msg:list, options:list, *args:str):
    for arg in args:
        msg.append(arg)
        options.append(arg[1])

def randint_list(floor, top, lstlen=None):
    '''Return list of length `lstlen` of random numbers in range from `floor` to `top`, including both'''
    lst = []
    lstlen = lstlen if lstlen != None else top-floor+1
    if top - floor + 1 >= lstlen:
        while len(lst) < lstlen:
            a = randint(floor, top)
            if a not in lst:
                lst.append(a)
    return lst

def end_join(iterable, sep:str=' ', end:str=' ') -> str:
    return end.join([sep.join(iterable[:-1]), iterable[-1]])

def poker_deal_cards(player_count):
    return [DECK[i] for i in randint_list(0, 51, player_count*2 + 5)]

def fancy_cards(lst):
    '''Return "fancy" string consisting of cards from list'''
    return ' | '.join(['',*[str(a)+' of '+str(b) for a,b in lst],'']).strip() if len(lst) else ''

def compare_combinations(combinations:list[dict]):
    '''Return best combination of `combinations`'''
    if len(combinations) == 1:
        return combinations[0]
    def _compare(lst1,lst2):
        '''"True" if lst1 is bigger than lst2, "False" if less, "None" if they're equal\n\n[3,2,1] is bigger than [3,2,0] or [3,1,10], and [2,3] is bigger than [1,10]'''
        list_to_int = lambda lst: reduce(lambda res, el: res*16 + el, lst, 0)
        return None if list_to_int(lst1) == list_to_int(lst2) else list_to_int(lst1) > list_to_int(lst2)
    initial = combinations[0]

    for comb in combinations[1:]:
        if comb['Cost'][0] > initial['Cost'][0]:
            initial = comb
        elif comb['Cost'][0] == initial['Cost'][0]:
            if comb['Cost'][0] in range(5, 11):
                if _compare(comb['Cost'], initial['Cost']) == True:
                    initial = comb
            else:
                if _compare(comb['Cost'], initial['Cost']) == True:
                    initial = comb
                elif _compare(comb['Cost'], initial['Cost']) == None:
                    if comb['Kicker'] == initial['Kicker'] == None: # Here
                        initial = comb
                    elif _compare(comb['Kicker'], initial['Kicker']):
                        initial = comb
    return initial

def __holdem_combination(cards:list[tuple]):
    '''Return the best possible Texas Hold'em Poker hand of available with input cards'''
    if not 1 <= len(cards) <= 7: raise ValueError('Wrong card quantity, maybe it\'s an Omaha hand?')
    def nom_sort(lst:list,acc=[]):
        '''Sorts card nominals in descending order using Bubblesort (I think it's a Bubblesort)'''
        if len(lst) <= 1: return acc + lst
        res = reduce(lambda res, i: lst[i] if ORDER.index(lst[i]) > ORDER.index(res) else res, range(len(lst)),2)
        del lst[lst.index(res)]
        return nom_sort(lst,acc + [res])

    def _sort_by_quantity(cards:list[tuple]):
        '''Return list of (nominal,quantity) in descending order of quantities and descending order of nominals with equal quantities in it'''
        card_noms = [x[0] for x in cards]
        table = [(nom, card_noms.count(nom)) for nom in {*card_noms}]
        lst = reduce(lambda res, t: res + [a for a in table if a[1] == t], range(4,0,-1), [])
        res = []
        for quantity in range(4,0,-1):
            cards_c = list(filter(lambda x: x[1] == quantity,lst))
            lst_c = nom_sort([a[0] for a in cards_c])
            res += reduce(lambda res,i: res + [a for a in cards_c if a[0] == lst_c[i]],range(len(lst_c)),[])
        return res

    lst = _sort_by_quantity(cards)
    decompressed_lst = reduce(lambda res, x: res + x, [[a[0]]*a[1] for a in lst], [])
    quants = [a[1] for a in lst]

    suits_list = [a[1] for a in cards]
    suits_quantities = list(map(lambda x: (x,suits_list.count(x)),{*suits_list}))
    '''
    10 Flush Royale
    9  Straight flush
    8  Four
    7  Full House
    6  Flush
    5  Straight
    4  Set
    3  Two pairs
    2  Pair
    1  Higher card
    '''
    temp = 0
    res = {'Hand' : None, 'Kicker' : None, 'Cost' : [0]}
    def add_kicker(lst): return [ORDER.index(param) for param in lst] if len(decompressed_lst) == 7 else None
    sjoin = lambda args: ''.join(str(arg) for arg in args)
    _k_in_k = lambda k1,k2: sjoin(k1) in sjoin(k2)

    if any(count in [a[1] for a in suits_quantities] for count in [5,6,7]):
        same_suits = nom_sort([card[0] for card in cards if any(a[1] >= 5 for a in suits_quantities if a[0] == card[1])])
        if len(same_suits) >= 5:
            # 9 Straight Flush
            if any(_k_in_k(same_suits[i:i+5],ORDER[::-1]) or (_k_in_k(same_suits[i+1:i+5]+['A'],ORDER[::-1]+['A']) and ('A' in same_suits)) for i in range(len(same_suits[4:]))):
                for i in range(len(same_suits)-4):
                    if _k_in_k(same_suits[i:i+5],ORDER[::-1]):
                        if same_suits[i] == 'A':
                            # 10 Flash Royale
                            res['Hand'] = f'Royal Flush: A to 10 {[a[0] for a in suits_quantities if a[1] >= 5][0]}'
                            res['Cost'] = [10]
                        else:
                            res['Hand'] = f'Straight Flush: {same_suits[i]} to {same_suits[i+4]} {[a[0] for a in suits_quantities if a[1] >= 5][0]}'
                            res['Cost'] = [9,ORDER.index(same_suits[i])]
                        break

                    if (_k_in_k(same_suits[i+1:i+5] + ['A'], ORDER[::-1] + ['A'])) and ('A' in same_suits):
                        res['Hand'] = f'Straight Flush: 5 to A {[a[0] for a in suits_quantities if a[1] >= 5][0]}'
                        res['Cost'] = [9,3]
                        break

            # 6 Flush
            else:
                res['Hand'] = f'Flush: {"-".join([ str(a) for a in same_suits[:5]])} {[a[0] for a in suits_quantities if a[1] >= 5][0]}'
                res['Cost'] = [6] + [ORDER.index(a) for a in same_suits[:5]]


    elif len(quants) >= 5:
        temp = nom_sort([a[0] for a in lst])
        # 5 Straight
        if any(_k_in_k(temp[i:i+5], ORDER[::-1]) or (_k_in_k(temp[i+1:i+5]+['A'], ORDER[::-1]+['A']) and 'A' in temp) for i in range(len(temp) - 4)):
            for i in range(len(temp)-4):
                if _k_in_k(temp[i:i+5],ORDER[::-1]):
                    res['Hand'] = f'Straight: {temp[i]} to {temp[i+4]}'
                    res['Cost'] = [5,ORDER.index(temp[i])]
                    break

                if (_k_in_k(temp[i+1:i+5] + ['A'],ORDER[::-1] + ['A'])) and ('A' in temp):
                    res['Hand'] = f'Straight: 5 to A'
                    res['Cost'] =[5,3]
                    break

    if res['Cost'][0] > 8:
        return res

    # 8 Four of a kind
    elif quants.count(4) > 0:
        res['Hand'] = f'Four of {lst[0][0]}\'s'
        res['Kicker'] = add_kicker([nom_sort(decompressed_lst[4:])[0]])
        res['Cost'] = [8,ORDER.index(lst[0][0])]

    if quants.count(3) > 0:
        # 7 Full House
        if (quants.count(3) == 2 or quants.count(2) >= 1) and res['Cost'][0] < 7:
            temp = nom_sort([item for item in decompressed_lst[3:] if any(a[1] >= 2 and a[0] == item for a in lst)])[0]
            res['Hand'] = f'Full House: set of {lst[0][0]}\'s and a pair of {temp}\'s'
            res['Cost'] = [7,ORDER.index(lst[0][0]),ORDER.index(temp)]

        # 4 Set
        elif res['Cost'][0] < 4:
            res['Hand'] = f'Set of {lst[0][0]}\'s'
            res['Kicker'] = add_kicker([lst[1][0],lst[2][0]])
            res['Cost'] = [4,ORDER.index(lst[0][0])]

    elif quants.count(2) > 0 and res['Cost'][0] < 3:
        # 3 Two pairs
        if quants.count(2) >= 2:
            temp = nom_sort([item for item in decompressed_lst if any(a[1] == 2 and a[0] == item for a in lst)])
            res['Hand'] = f'Two Pairs: a pair of {temp[0]}\'s and a pair of {temp[2]}\'s'
            res['Kicker'] = add_kicker([nom_sort(decompressed_lst[4:])[0]])
            res['Cost'] = [3,ORDER.index(temp[0]),ORDER.index(temp[2])]

        # 2 Pair
        else:
            temp = nom_sort([item for item in decompressed_lst if any(a[1] == 2 and a[0] == item for a in lst)])[0]
            res['Hand'] = f'Pair of {temp}\'s'
            res['Kicker'] = add_kicker(decompressed_lst[2:5])
            res['Cost'] = [2,ORDER.index(temp)]

    # 1 Highcard
    elif res['Cost'][0] < 1:
        temp = nom_sort([a[0] for a in cards])
        res['Hand'] = f'Highcard {temp[0]} {[card[1] for card in cards if card[0] == temp[0]][0]}'
        res['Kicker'] = add_kicker(temp[1:5])
        res['Cost'] = [1,ORDER.index(temp[0])]


    return res

def __omaha_combination(player_cards:list[tuple], table_cards:list[tuple]) -> dict:
    combinations = []
    player_vars = list(iter_combs(range(4), 2))
    table_vars = list(iter_combs(range(len(table_cards)), 3))
    if len(table_cards) == 0:
        return compare_combinations([__holdem_combination([player_cards[var[0]], player_cards[var[1]]]) for var in player_vars])
    else:
        for p_var in player_vars:
            for t_var in table_vars:
                combinations.append(__holdem_combination([player_cards[i] for i in p_var] + [table_cards[e] for e in t_var]))
    return compare_combinations(combinations)

def poker_combination(player_cards:list[tuple], table_cards:list[tuple], game_type='T'):
    if game_type == "T":
        return __holdem_combination(player_cards + table_cards)
    elif game_type == "O":
        return __omaha_combination(player_cards, table_cards)
    else:
        raise ValueError('g_type must be one of "T", "O"')

def f_all(output, lst:list, kwarg=None, *values) -> list:
    '''Return list of `output` parameter of items in `lst` if item.`kwarg` (or item[`kwarg`]) equals any of values'''
    if all(isinstance(a, (int, str, float, tuple)) for a in lst):
        raise TypeError(f'Expected a dict or object, got another')
    if all(isinstance(a, dict) for a in lst):
        return [a[output] if output != 'self' else a for a in lst if ((a[kwarg] in values) if kwarg != None else True)]
    elif all(isinstance(a, object) for a in lst):
        return [getattr(item, output) if output != 'self' else item for item in lst if ((getattr(item, kwarg) in values) if kwarg != None else True)]

# def f_all(output, lst, kwarg=None, values:list=None): # This is basically Excel at this point
#     result = []
#     if isinstance(lst, (list, tuple)):
#         for elem in lst:
#             if (kwarg, values) != (None, None):
#                 if all(attr in dir(elem) for attr in [kwarg, output]):
#                     result += [elem.output] if elem.kwarg in values else []
#                 elif isinstance(elem, dict) and (kwarg in elem.keys() and elem[kwarg] == values)




def shuffle_lst(lst:list):
    x = randint_list(0,len(lst)-1)
    for i in range(len(lst)):
        lst += [lst[x[i]]]
    return lst[len(lst)//2:]

def share_the_pot(pot, p_list:list) -> int:
    '''Share pot between players'''
    for p in p_list:
        p.bankroll += pot // len(p_list)

# Server stuff
class sync_conn:
    '''Special class consisting of functions used to send to/ask for input from players and for players to recieve and/or answer'''

    def print(socks_or_players: list, msg: str):
        '''Send a message to all players from `players`'''
        for elem in socks_or_players:
            if not isinstance(elem, socket.socket):
                elem = elem.connect["Connection"]
            elem.send('print'.encode())
            elem.recv(1024)
            elem.send(msg.encode())

    def input(__sock_or_player, msg: str):
        '''ask particular player for input, return it'''
        if msg != None:
            if not isinstance(__sock_or_player, socket.socket):
                __sock_or_player = __sock_or_player.connect["Connection"]
            __sock_or_player.send('input'.encode())
            __sock_or_player.recv(1024)
            __sock_or_player.send(msg.encode())
            return __sock_or_player.recv(1024).decode()

    def send_custom(sock: socket.socket, msg_type: str, msg: str=None): # hope it'll be used in future
        '''send a message with a special marker'''
        if msg_type not in ['close','marker','clear']:
            raise ValueError
        else:
            sock.send(msg_type.encode())
            sock.recv(1024)
            sock.send(msg.encode())

    def receive(sock:socket.socket, marker=None):
        if marker == None:
            marker = sock.recv(1024).decode()
            sock.send('received'.encode())
        data = sock.recv(1024).decode()
        if marker in ['print', 'close']:
            print(data)
        elif marker == 'input':
            sock.send(input(data).encode())
        return marker == 'close'

class PokerPlayer:
    current_bet = 0
    flag_active:bool = True
    flag_out:bool = False
    flag_dealer:bool = False
    did_move:bool = False

    def __init__(self, name:str, place:int=-1, connect={}, bankroll:int=1000) -> None:
        self.name = name
        self.cards:list[tuple] = []
        self.place = place
        self.connect = connect
        self.bankroll = bankroll

    def bet(self, bet, blind:str=None):
        self.current_bet = min(self.bankroll, bet)
        if self.current_bet == self.bankroll:
            return f'\n{self.name} goes all-in ({self.current_bet}$)!'
        result = f'\n{self.name} bets {self.current_bet}$'
        if blind != None:
            result += f' as a {blind.lower()} blind'
        else:
            self.did_move = True
        return result

    def action(self, bet=0, small_blind=10) -> str:
        self.did_move = True
        if self.flag_active and self.bankroll > 0:
            msg = []
            options = []
            if bet <= self.current_bet:   add_to(msg,options,'[C]heck')
            else:
                if self.bankroll > bet:
                    add_to(msg, options, '[C]all')
                else:
                    add_to(msg, options, '[A]ll-in')
            if bet == 0:                  add_to(msg,options,'[B]et')
            elif self.bankroll > 2*bet:   add_to(msg,options,'[R]aise')
            add_to(msg, options, '[F]old', '[Q]uit')

            #Ask for a move
            name = sync_conn.input(self, f'\n{self.name}, Your move;\n{end_join(msg,", "," or ")}\n> ').upper()
            while name not in options:
                sync_conn.print(self, '\nIncorrect move! Please, try again:')
                name = sync_conn.input(self, f'\n{self.name}, Your move;\n{end_join(msg,", "," or ")}\n> ').upper()

            # The move itself
            if name == 'C':
                if bet == self.current_bet:
                    return f'\n{self.name} checks'
                else:
                    self.current_bet = bet
                    return f'\n{self.name} calls'

            elif name == 'F':
                self.flag_active = False
                return f'\n{self.name} folds'

            elif name == 'Q':
                self.flag_out = True
                self.flag_active = False
                return f'\n{self.name} quits'

            elif name == 'A':
                return self.bet(self.bankroll)

            elif name in 'BR':
                minimum = max(bet, small_blind*4) if name == 'R' else small_blind*2
                new_bet = sync_conn.input(self, f'Enter a bet ({minimum} to {self.bankroll}$ or [A]ll-in):\n> ').capitalize()
                while new_bet not in (['A'] if name in 'B' else []) + [str(a) for a in range(minimum, self.bankroll + 1)]:
                    sync_conn.print(self, 'Incorrect input.\n')
                    new_bet = sync_conn.input(self, f'Enter a bet ({minimum} to {self.bankroll}$ or [A]ll-in):\n> ').capitalize()
                if new_bet.upper() == 'A':
                    return self.bet(self.bankroll)
                return self.bet(int(new_bet))

class PokerTable:
    viewers = []
    def __init__(self, *players:PokerPlayer) -> None:
        self.players: list[PokerPlayer] = list(players)
        self.active_players = players
        self.current_pot = 0

    def default_state(self):
        for player in self.players:
            player.flag_active = True
            player.flag_out = False
            player.bankroll = 1000

    def party(self, small_blind, game_type):

        def showdown(table: list[tuple]):
            indexes = []
            combs = []
            def ask(player:PokerPlayer):
                sync_conn.print(self.viewers, f'\n{player.name}\'s move')
                if sync_conn.input(player, f'{player.name}, would You like to show your cards (Y/N)?\n').upper() == 'Y':
                    sync_conn.print(self.viewers, f'\n{player.name}\'s cards are {fancy_cards(player.cards)}')
                    sync_conn.print(self.viewers, f'The best hand: {poker_combination(player.cards, table, game_type)["Hand"]}')
                    indexes.append(self.active_players.index(player))
                    combs.append(poker_combination(player.cards, table, game_type))
                else:
                    sync_conn.print(self.viewers, f'{player.name} passes his cards')
            for p in self.active_players[:-1]:
                ask(p)
            if len(indexes) == 0:
                indexes.append(-1)
                combs.append(poker_combination(self.active_players[-1].cards, table, game_type))
            else:
                ask(self.active_players[-1])
            return indexes, combs

        def check_the_bets(bet):
            '''Return bool((all called / all-in'ed) and (all did a move))'''
            return all((p.current_bet == bet or p.current_bet == p.bankroll or not p.flag_active) and (p.did_move) for p in self.active_players)

        # preparations
        dealer_place = f_all('place', self.players, 'flag_dealer', True)[0]
        game_coeff = ["T", "O"].index(game_type)

        # initial state
        session_cards = poker_deal_cards(len(self.players)*(1 + game_coeff))
        table_cards = session_cards[-5:]
        for player in self.players:
            player.cards = session_cards[(2 + 2*game_coeff)*self.players.index(player) : (2 + 2*game_coeff)*(self.players.index(player) + 1)]
            player.flag_active = True
        self.active_players = self.players

        # rounds
        session_state = 0  # 0 - preflop(0), 1 - flop(3), 2 - turn(4), 3 - river(5)
        best_current_hand = lambda p: poker_combination(p.cards, visible_table_cards, game_type)

        while session_state <= 3 and len([p for p in self.active_players if p.flag_active and p.bankroll]) > 1 and len(self.active_players) > 1:
            # counter = 0
            visible_table_cards = table_cards[0:(lambda x: int(2*bool(x) + x))(session_state)]
            sync_conn.print(self.viewers, '= '*25)
            sync_conn.print(self.viewers, f'Players: {" - ".join([p.name + f"[{str(p.bankroll)}$]" + "[D]"*p.flag_dealer + "[X]"*(not p.flag_active) for p in self.players])}')
            sync_conn.print(self.viewers, f'Current pot: {self.current_pot}$')
            sync_conn.print(self.viewers, f'\nTable: {fancy_cards(visible_table_cards)}')
            for player in self.active_players:
                sync_conn.print(player, f'Your cards: {fancy_cards(player.cards)}')
                sync_conn.print(player, f'Strongest hand: {best_current_hand(player)["Hand"]}')
            bet = 0
            if session_state == 0:
                sync_conn.print(self.viewers, self.players[(dealer_place + 1) % len(self.players)].bet(small_blind, 'small'))
                sync_conn.print(self.viewers, self.players[(dealer_place + 2) % len(self.players)].bet(small_blind*2, 'big'))
                bet = max(f_all('current_bet', self.players))
                counter = (dealer_place + 3) % len(self.players)

            while (counter < len(self.players) or not check_the_bets(bet)) and len(self.active_players) > 1:
                current_player = self.players[counter % len(self.players)]
                if current_player.bankroll and current_player.flag_active:
                    sync_conn.print([p for p in self.viewers if p != current_player], f'\nIt\'s {current_player.name}\'s move')
                sync_conn.print(self.viewers, self.players[counter % len(self.players)].action(bet, small_blind))
                bet = max(f_all('current_bet', self.players))
                self.active_players = list(filter(lambda p: p.flag_active and not p.flag_out, self.players))
                if len(self.active_players) == 1:
                    break
                counter += 1

            for player in self.players:
                player.did_move = False
                if bet > 0:
                    self.current_pot += player.current_bet
                    player.bankroll -= player.current_bet
                    player.current_bet = 0
            session_state += 1

        # showdown
        visible_table_cards = table_cards
        if len(self.active_players) > 1:
            sync_conn.print(self.viewers, f'\nTable: {fancy_cards(table_cards)}')
            indexes, hands = showdown(table_cards)
            if len(hands) == 1:
                sync_conn.print(self.viewers, f'\nPlayer {self.active_players[indexes[0]].name} wins!')
                share_the_pot(self.current_pot, [self.active_players[indexes[0]]])
            else:
                winner_hand = compare_combinations(hands)
                winners = [(p, best_current_hand(p)['Kicker'] == winner_hand['Kicker']) for p in self.active_players if best_current_hand(p)['Cost'] == winner_hand['Cost']]
                if len(winners) > 1:
                    winner_names = [nam[0].name for nam in winners if nam[1]]
                    if len(winner_names) > 1:
                        sync_conn.print(self.viewers, f'\nA tie! {end_join(winner_names,", "," and ")} share the pot equally, as they have the same highest combination:\n{winner_hand["Hand"]}')
                    else:
                        sync_conn.print(self.viewers, f'\nPlayer {winner_names[0]} wins the round,\nhis hand had the highest kicker: {", ".join([str(ORDER[x]) for x in winner_hand["Kicker"]])}')
                else:
                    sync_conn.print(self.viewers, f'\nPlayer {winners[0][0].name} wins with the strongest combination:\n{best_current_hand(winners[0][0])["Hand"]}')
                share_the_pot(self.current_pot, [a[0] for a in winners if a[1]])
        else:
            sync_conn.print(self.viewers, f'\nPlayer {self.active_players[0].name} wins!')
            share_the_pot(self.current_pot, self.active_players)
        self.current_pot = 0

        [p for p in self.players if p.flag_dealer][0].flag_dealer = False
        self.players = list(filter(lambda a: a.bankroll > 0 and not a.flag_out, self.players))
        ([p for p in self.players if p.place > dealer_place]+[self.players[0]])[0].flag_dealer = True
        # The end

    def game_of_poker(self, game_type = "T"):
        self.viewers = self.players
        __small_blind = 10
        rounds = 0
        self.players[0].flag_dealer = True
        print('Game starts')
        while len(self.players) > 1:
            small_blind = __small_blind << (rounds // 4)
            self.party(small_blind, game_type)
            rounds += 1
        sync_conn.print(self.viewers, f"\nGame is finished, winner - {self.players[0].name}")
        sync_conn.print(self.viewers, 'Waiting for host to restart or leave...')
        print('Game has ended\n')
        self.players = self.viewers
        self.default_state()


__all__ = ['sync_conn', 'DECK', 'PokerPlayer', 'PokerTable', 'fancy_cards', 'f_all', 'ORDER', 'shuffle_lst', 'end_join', 'SUITS']