from enum import Enum
from src.model.game import Game
from src.model.game.impl import GameCore


class GamePhase(Enum):
    WAITING_FOR_PLAYERS = 1
    PLAYING = 2
    PLAYERS_TURN = 3
    GAME_OVER = 4


class GameImpl(Game):

    def __init__(self):
        self.phase = GamePhase.WAITING_FOR_PLAYERS
        self.core = GameCore()
    
    def addPlayer(self, player):
        if self.phase != GamePhase.WAITING_FOR_PLAYERS:
            raise ValueError("Cannot add player while game is running")
        self.core.addPlayer(player)
    
    def removePlayer(self, player):
        if (self.phase != GamePhase.WAITING_FOR_PLAYERS and self.phase != GamePhase.PLAYERS_TURN) or self.core.getCurrentPlayer() != player:
            raise ValueError("Cannot remove player while it is not their turn")
        self.core.removePlayer(player)
        if len(self.core.getPlayers()) == 1:
            self.phase = GamePhase.GAME_OVER
        else:
            self.phase = GamePhase.PLAYING

    def startGame(self):
        if self.phase != GamePhase.WAITING_FOR_PLAYERS:
            raise ValueError("Cannot start game while game is running")
        self.core.startGame()
        self.phase = GamePhase.PLAYING

    def startRound(self):
        if self.phase != GamePhase.PLAYING:
            raise ValueError("Cannot start round in this phase")
        self.core.startRound()
        self.phase = GamePhase.PLAYERS_TURN

    def raiseStake(self, stake):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot raise stake while it is not the player's turn")
        self.core.raiseStake(stake)
        
    def checkLiar(self):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot check liar while it is not the player's turn")
        loser = self.core.checkLiar()
        if not loser.cardsInHand > GameCore.MAX_CARDS:
            self.phase = GamePhase.PLAYING
        else:
            self.removePlayer(loser)
        return loser
    
    def getPlayers(self):
        return self.core.getPlayers()
    
    def getCurrentPlayer(self):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot get current player while it is not the player's turn")
        return self.core.getCurrentPlayer()
    
    def getLatestStake(self):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot get latest stake while it is not the player's turn")
        return self.core.getLatestStake()

    def getPhase(self):
        return self.phase
    

    
