from typing import Protocol
from model.deck import Stake
from model.player import Player


class Game(Protocol):
    def startTurn(self) -> None:
        ...

    def raiseStake(self, stake) -> None:
        ...
    
    def checkLiar(self) -> bool:
        ...
    
    def getCurrentPlayer(self) -> Player:
        ...

    def getLatestStake() -> Stake:
        ...