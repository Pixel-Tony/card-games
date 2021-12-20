import socket
from util.poker_util import *

class DurakPlayer:
    def __init__(self, name:str, connect:socket.socket) -> None:
        self.name = name
        self.cards = []
        self.connect = connect

    def has_cards(self):
        return len(self.cards) > 0

    def move(self):
        pass

class DurakGame:
    players:list[DurakPlayer] = []
    def __init__(self) -> None:
        pass

    def durak_game(self):
        game_deck = shuffle_lst(DECK)
        def add_up_cards(players:list[DurakPlayer]):
            while any(len(player.cards) < 6 for player in players) and len(game_deck) > 0:
                for player in self.players:
                    player.cards += [game_deck.pop(0)]
                    if len(game_deck) == 0:
                        break

        while len(list(filter(lambda p: len(p.cards) > 0, self.players))) > 1:
            counter = 0




            pass









game = DurakGame()
for name in ['John', 'Tina', 'Bob']:
    game.players += [DurakPlayer(name, 'test')]

game.durak_game()