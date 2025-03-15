from typing import Protocol
from src.model.player import Player
from src.model.stake import Stake


class Game(Protocol):
    def add_player(self, player:Player) -> None:
        ...
    
    def remove_player(self, player:Player) -> None:
        ...
        
    def start_game(self) -> None:
        ...

    def start_round(self) -> None:
        ...

    def raise_stake(self, stake:Stake) -> Stake:
        ...
    
    def check_liar(self) -> Player:
        ...
    
    def get_players(self) -> list[Player]:
        ...
    
    def get_current_player(self) -> Player:
        ...

    def get_latest_stake(self) -> Stake:
        ...
    
    