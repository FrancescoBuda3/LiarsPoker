from typing import Protocol
from src.model.player import Player
from src.model.stake import Stake


class Game(Protocol):
    def addPlayer(self, player:Player) -> None:
        ...
    
    def removePlayer(self, player:Player) -> None:
        ...
        
    def startGame(self) -> None:
        ...

    def startRound(self) -> None:
        ...

    def raiseStake(self, stake:Stake) -> None:
        ...
    
    def checkLiar(self) -> Player:
        ...
    
    def getPlayers(self) -> list[Player]:
        ...
    
    def getCurrentPlayer(self) -> Player:
        ...

    def getLatestStake(self) -> Stake:
        ...
    
    