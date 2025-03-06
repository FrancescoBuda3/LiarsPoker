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
        ...

    def startGame(self):
        ...

    def startRound(self):
        ...

    def raiseStake(self, stake):
        ...
    
    def checkLiar(self):
        ...
    
    def getPlayers(self):
        ...
    
    def getCurrentPlayer(self):
        ...
    
    def getLatestStake(self):
        ...
    

    
