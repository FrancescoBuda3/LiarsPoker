from ..game import *
from src.utils.debug.impl import Debuggable
from src.model.deck.impl import DeckImpl
from src.model.player import Player


class GameImpl(Game, Debuggable):
    STARTING_PLAYER_INDEX = 0
    STARTING_CARDS = 1
    MINIMUM_PLAYERS = 2

    def __init__(self, debug: bool = True):
        Debuggable.__init__(self, debug)
        self.players = []
        self.deck = DeckImpl()
        self.currentPlayerIndex = self.STARTING_PLAYER_INDEX
        self.lastestStake = None

    def addPlayer(self, player:Player):
       player.cardsInHand = self.STARTING_CARDS
       self.players.append(player)

    def startTurn(self) -> None:
        if len(self.players) < self.MINIMUM_PLAYERS:
            raise ValueError("Cannot start without enough players")
        else :
            hands = self.deck.shuffle(player.cardsInHand for player in self.players)
            for i, hand in enumerate(hands):
                self.players[i].cards = hand

    def getCurrentPlayer(self): return self.players[self.currentPlayerIndex]
    
    def raiseStake(self, stake) : self.lastestStake = stake
    
    def getLatestStake(self): return self.lastestStake
        
    

        