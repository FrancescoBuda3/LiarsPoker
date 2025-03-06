from ..game import *
from src.model.deck.impl import DeckImpl
from src.model.player import Player
from src.model.stake.impl import StakeHandlerImpl




class GameCore(Game):
    STARTING_PLAYER_INDEX = 0
    STARTING_CARDS = 1
    MINIMUM_PLAYERS = 2
    MAX_CARDS = 5

    def __init__(self):
        self.players = []
        self.deck = DeckImpl()
        self.currentPlayerIndex = self.STARTING_PLAYER_INDEX
        self.stakeHandler = StakeHandlerImpl()

    def startGame(self):
        if len(self.players) < self.MINIMUM_PLAYERS:
            raise ValueError("Cannot start without enough players")
        self.startRound()

    def addPlayer(self, player:Player):
        player.cardsInHand = self.STARTING_CARDS
        self.players.append(player)

    def removePlayer(self, player:Player):
        self.currentPlayerIndex = self.__next_player_index()
        self.players.remove(player)

    def startRound(self) -> None:
        hands = self.deck.shuffle(player.cardsInHand for player in self.players)
        for i, hand in enumerate(hands):
            self.players[i].cards = hand

    def __next_player_index(self): return (self.currentPlayerIndex + 1) % len(self.players)

    def __previous_player_index(self): return (self.currentPlayerIndex + len(self.players) - 1) % len(self.players)

    def getCurrentPlayer(self): return self.players[self.currentPlayerIndex]

    def getPlayers(self): return self.players
    
    def raiseStake(self, stake) :
        self.stakeHandler.set_stake(stake)
        self.currentPlayerIndex = self.__next_player_index()
    
    def getLatestStake(self): return self.stakeHandler.get_stake()

    def checkLiar(self):
        hands = [player.cards for player in self.players]
        cards = [card for hand in hands for card in hand]
        isLiar = not self.stakeHandler.check_cards(cards)
        loser_index = self.__previous_player_index() if isLiar else self.currentPlayerIndex
        self.currentPlayerIndex = loser_index
        self.players[loser_index].cardsInHand += 1
        return self.players[loser_index]

        
    

        