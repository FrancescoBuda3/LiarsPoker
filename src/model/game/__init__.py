from typing import Protocol
from src.model.deck import Stake
from src.model.player import Player


class Game(Protocol):
    def startTurn(self) -> None:
        ...

    def raiseStake(self, stake:Stake) -> None:
        ...
    
    def checkLiar(self) -> bool:
        ...
    
    def getCurrentPlayer(self) -> Player:
        ...

    def getLatestStake() -> Stake:
        ...
    
    def addPlayer(self, player:Player) -> None:
        ...