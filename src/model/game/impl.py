from ..game import *
from src.utils.debug.impl import Debuggable
from src.model.deck import generate_deck
from src.model.player import Player


class GameImpl(Game, Debuggable):
    def __init__(self, debug: bool = True):
        Debuggable.__init__(self, debug)
        self.players = []
        self.deck = generate_deck()
        self.turn = 0

    def addPlayer(self, player:Player):
       player.cardsInHand = 1
       self.players.append(player)

    def startTurn(self) -> None:
        if len(self.players) < 2:
            raise ValueError("Cannot start without players")
        else :
            hands = self.deck.shuffle(player.cardsInHand for player in self.players)
            for i, hand in enumerate(hands):
                self.players[i] = hand

    

        