from typing import Protocol
from uuid import UUID

from src.model.card import Card
from src.model.player import Player
from src.model.stake import Stake
from src.services.message import Message


class MessageFactoryInterface(Protocol):
    def create_show_cards_message(self, cards: list[Card]) -> Message:
        """
        Create a message to show the cards currently in game.

        Args:
            cards (list[Card]): list of cards to be shown

        Returns:
            Message: the constructed message
        """
        ...

    def create_start_turn_message(self, player: Player, minimum_stake: Stake) -> Message:
        """
        Create a message to start the turn for a player.

        Args:
            player (Player): player to start the turn for
            minimum_stake (Stake): minimum stake to play

        Returns:
            Message: the constructed message
        """
        ...

    def create_start_round_message(self, players: list[Player]) -> Message:
        """
        Create a message to start a round.

        Args:
            players (list[Player]): list of players in the round

        Returns:
            Message: the constructed message
        """
        ...

    def create_round_loser_message(self, player: Player) -> Message:
        """
        Create a message to notify the loser of the round.

        Args:
            player (Player): player who lost the round

        Returns:
            Message: the constructed message
        """
        ...

    def create_elimination_message(self, player: Player) -> Message:
        """
        Create a message to notify the elimination of a player.

        Args:
            player (Player): player who was eliminated

        Returns:
            Message: the constructed message
        """
        ...

    def create_game_over_message(self, player: Player) -> Message:
        """
        Create a message to notify the game over.

        Args:
            player (Player): player who won the game

        Returns:
            Message: the constructed message
        """
        ...

    def create_raise_stake_message(self, stake: Stake) -> Message:
        """
        Create a message to raise the stake.

        Args:
            stake (Stake): new stake

        Returns:
            Message: the constructed message
        """
        ...

    def create_check_liar_message(self) -> Message:
        """
        Create a message to check if the last stake is a lie.

        Returns:
            Message: the constructed message
        """
        
    def create_new_player_message(self, player: str, id: UUID) -> Message:
        """
        Create a message to create a new player.

        Args:
            player (Player): new player

        Returns:
            Message: the constructed message
        """
        ...
        
    def create_new_lobby_message(self, player_id: UUID, lobby_id: int) -> Message:
        """
        Create a message to create a new lobby.

        Args:
            player_id (UUID): ID of the player
            lobby_id (int): ID of the lobby

        Returns:
            Message: the constructed message
        """
        ...
        
    def create_join_lobby_message(self, player_id: UUID, lobby_id: int) -> Message:
        """
        Create a message to join a lobby.

        Args:
            player_id (UUID): ID of the player
            lobby_id (int): ID of the lobby

        Returns:
            Message: the constructed message
        """
        ...
