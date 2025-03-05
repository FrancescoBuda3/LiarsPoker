from ..game import *
from src.model.deck.impl import DeckImpl
from src.model.player import Player
from src.model.stake.impl import StakeHandlerImpl


class GameImpl(Game):
    STARTING_PLAYER_INDEX = 0
    STARTING_CARDS = 1
    MINIMUM_PLAYERS = 2

    def __init__(self):
        self.players = []
        self.deck = DeckImpl()
        self.currentPlayerIndex = self.STARTING_PLAYER_INDEX
        self.stakeHandler = StakeHandlerImpl()

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
    
    def raiseStake(self, stake) :
        self.stakeHandler.set_stake(stake)
        self.currentPlayerIndex = (self.currentPlayerIndex + 1) % len(self.players)
    
    def getLatestStake(self): return self.stakeHandler.get_stake()

    def checkLiar(self):
        hands = [player.cards for player in self.players]
        cards = [card for hand in hands for card in hand]
        return self.stakeHandler.check_cards(cards)
        
    

        