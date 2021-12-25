import socket
from typing import Literal, Union
from util.poker_util import *
import asyncio


class async_conn:
    async def input(socks_or_players:list[Union['DurakPlayer', socket.socket]], msg: str, table_cards=None):
        '''ask particular player(s) for input, return it'''
        for player in socks_or_players:
            if not isinstance(player, socket.socket):
                player = player.connect['Connection']
            player.send('multi-input'.encode())
            player.recv(1024)
            player.send(msg.encode())
            return player.recv(1024).decode()

    def recieve(sock:socket.socket):
        def __send_cards(player:DurakPlayer, table_cards=[]):
            available_cards = list(filter(lambda card: card[0] in [*zip(*table_cards)][0], player.cards))

            NotImplementedError
            pass

        marker = sock.recv(1024).decode()
        sock.send('received'.encode())
        if marker in ['print', 'input', 'close']:
            sync_conn.receive(sock, marker)
        elif marker == 'multi-input':
            data = sock.recv(1024).decode()

        NotImplementedError
        pass


class DurakPlayer:
    def __init__(self, name:str, connect:dict[str , socket.socket]) -> None:
        self.name = name
        self.cards:list = []
        self.connect = connect

    def move(self, attacker_cards=None, table_cards=None, **kwargs):
        # if not attacker_cards:
        #     if 'first' in kwargs:
        #         sync_conn.input(self, f'Choose a card to move: {')
        pass

    # def move(self, attacker_cards=None, **kwargs) -> Union[list, str]:
    #     if attacker_cards == None:
    #         if 'first' in kwargs and kwargs['first'] == True:
    #             sync_conn.input(self, f'Choose a card to move: {"\n".join(self.cards)}')
    #         else:
    #             sync_conn.input(self, f'Choose a card to move:')
    #     pass



class DurakGame:
    players:list[DurakPlayer] = []

    def __init__(self) -> None:
        pass

    def durak_game(self, throws=True, shifts=False):
        def add_up_cards(players:list[DurakPlayer]):
            while any(len(player.cards) < 6 for player in players) and len(game_deck) > 0:
                for player in self.players:
                    player.cards += [game_deck.pop(0)]
                    if len(game_deck) == 0:
                        break

        game_deck = shuffle_lst(DECK)







        counter = 0
        while len(list(filter(lambda p: len(p.cards) > 0, self.players))) > 1:
            # __attacker = self.players[counter % len(self.players)]
            # __defender = self.players[(counter + 1) % len(self.players)]
            # __attacker_finished = False
            # __first = True
            # table_cards = []
            # while not __attacker_finished:
            #     attacker_cards = __attacker.move(first=__first)
            #     table_cards += attacker_cards
            #     __defender.move(attacker_cards)



            pass







game = DurakGame()
for name in ['John', 'Tina', 'Bob']:
    game.players += [DurakPlayer(name, 'test')]

game.durak_game()

__all__ = ['DurakPlayer']