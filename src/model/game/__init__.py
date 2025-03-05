from typing import Protocol
from src.model.player import Player
from src.model.stake import Stake


class Game(Protocol):
    def startTurn(self) -> None:
        ...

    def raiseStake(self, stake:Stake) -> None:
        ...
    
    def checkLiar(self) -> bool:
        ...
    
    def getCurrentPlayer(self) -> Player:
        ...

    def getLatestStake(self) -> Stake:
        ...
    
    def addPlayer(self, player:Player) -> None:
        ...