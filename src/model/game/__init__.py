from dataclasses import dataclass, replace
from datetime import datetime, timedeltas
from typing import Protocol

class game(Protocol):
    def start(self) -> None:
        ...

    def playTurn(self) -> None:
        ...
    
    def checkLiar(self) -> None:
        ...
    
    def end(self) -> None:
        ...