from ..game import *
from utils.debug.impl import _Debuggable


class GameImpl(Game, _Debuggable):
    def __init__(self, debug: bool = True):
        _Debuggable.__init__(self, debug)

    
    def start(self) -> None:
        ...

    def playTurn(self) -> None:
        ...
    
    def checkLiar(self) -> None:
        ...
    
    def end(self) -> None:
        ...
    
        