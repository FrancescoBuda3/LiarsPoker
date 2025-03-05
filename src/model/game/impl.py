from src.model.stake import StakeHandler
from ..game import *
from src.model.deck.impl import DeckImpl
from src.model.player import Player


class GameImpl(Game):
    STARTING_PLAYER_INDEX = 0
    STARTING_CARDS = 1
    MINIMUM_PLAYERS = 2

    def __init__(self):
        self.players = []
        self.deck = DeckImpl()
        self.currentPlayerIndex = self.STARTING_PLAYER_INDEX
        self.stakeHandler = StakeHandler()

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
    
    def raiseStake(self, stake) : self.stakeHandler.set_stake(stake)
    
    def getLatestStake(self): return self.stakeHandler.get_stake()
        
    

        