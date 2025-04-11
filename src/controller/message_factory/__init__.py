from typing import Protocol

from src.model.card import Card
from src.model.player import Player
from src.model.stake import Stake


class MessageFactoryInterface(Protocol):
    def create_show_cards_message(self, cards: list[Card]) -> str:
        """
        Create a message to show the cards currently in game.

        Args:
            cards (list[Card]): list of cards to be shown

        Returns:
            str: serialized message
        """
        ...

    def create_start_turn_message(self, player: Player, minimum_stake: Stake) -> str:
        """
        Create a message to start the turn for a player.

        Args:
            player (Player): player to start the turn for
            minimum_stake (Stake): minimum stake to play

        Returns:
            str: serialized message
        """
        ...

    def cerate_start_round_message(self, players: list[Player]) -> str:
        """
        Create a message to start a round.

        Args:
            players (list[Player]): list of players in the round

        Returns:
            str: serialized message
        """
        ...
        
    def create_round_loser_message(self, player: Player) -> str:
        """
        Create a message to notify the loser of the round.

        Args:
            player (Player): player who lost the round

        Returns:
            str: serialized message
        """
        ...
    
    def create_elimination_message(self, player: Player) -> str:
        """
        Create a message to notify the elimination of a player.

        Args:
            player (Player): player who was eliminated

        Returns:
            str: serialized message
        """
        ...
        
    def create_game_over_message(self, player: Player) -> str:
        """
        Create a message to notify the game over.

        Args:
            player (Player): player who won the game

        Returns:
            str: serialized message
        """
        ...
        
    def create_raise_stake_message(self, stake: Stake) -> str:
        """
        Create a message to raise the stake.

        Args:
            stake (Stake): new stake

        Returns:
            str: serialized message
        """
        ...
    
    def create_check_liar_message(self) -> str:
        """
        Create a message to check if the last stake is a lie.
        
        Returns:
            str: serialized message
        """
