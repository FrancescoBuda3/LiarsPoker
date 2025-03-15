from typing import Protocol
from src.model.player import Player
from src.model.stake import Stake


class Game(Protocol):
    def add_player(self, player:Player) -> None:
        """
        Adds a player to the game. to be called before the game starts.
        Args:
            player (Player): the player to add
        """
        ...
    
    def remove_player(self, player:Player) -> None:
        """
        Removes a player from the game.
        Args:
            player (Player): the player to remove
        """
        ...
        
    def start_game(self) -> None:
        """
        Starts the game, to be called after all players have been added.
        """
        ...

    def start_round(self) -> None:
        """
        Starts a new round of the game.
        """
        ...

    def raise_stake(self, stake:Stake) -> Stake:
        """
        Raises the stake of the game.
        Args:
            stake (Stake): the stake to raise
        Returns:
            Stake: the lowest stake that can be raised next
        """
        ...
    
    def check_liar(self) -> Player:
        """
        checks if the last stake was a lie.

        returns:
            Player: the player who lost the round
        """
        ...
    
    def get_players(self) -> list[Player]:
        """
        Returns the list of players in the game.
        Returns:
            list[Player]: the list of players
        """
        ...
    
    def get_current_player(self) -> Player:
        """
        Returns the current player.
        Returns:
            Player: the current player
        """
        ...

    def get_latest_stake(self) -> Stake:
        """
        Returns the latest stake.
        Returns:
            Stake: the latest stake
        """
        ...
    
    