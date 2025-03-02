from dataclasses import dataclass, replace
from typing import Protocol

class Game(Protocol):
    def start(self) -> None:
        ...

    def playTurn(self) -> None:
        ...
    
    def checkLiar(self) -> None:
        ...
    
    def end(self) -> None:
        ...