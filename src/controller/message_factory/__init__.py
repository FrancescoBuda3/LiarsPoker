from typing import Protocol
from uuid import UUID

from src.model.card import Card
from src.model.player import Player
from src.model.stake import Stake
from src.services.message import Message


class MessageFactoryInterface(Protocol):

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
    
    def create_game_info_message(self, interested_player: Player, players: list[Player], turn_player: Player, latest_stake: Stake, min_next_stake: Stake) -> Message:
        """
        Create a message with game info.

        Args:
            interested_player (Player): player who is interested in the game info
            players (list[Player]): list of players in the round
            turn_player (Player): player whose turn it is
            latest_stake (Stake): latest stake raised
            min_next_stake (Stake): minimum stake for the next player

        Returns:
            Message: the constructed message
        """
        ...

    def create_round_loser_message(self, player: Player, cards: list[Card], elimination: bool) -> Message:
        """
        Create a message to notify the loser of the round.

        Args:
            player (Player): player who lost the round
            cards (list[Card]): list of cards in game
            elimination (bool): true if the player was eliminated, false otherwise

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

    def create_raise_stake_message(self, player: Player, stake: Stake) -> Message:
        """
        Create a message to raise the stake.

        Args:
            player (Player): player who raised the stake
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
        ...

    def create_new_player_message(self, username: str, id: UUID, response: bool) -> Message:
        """
        Create a message to create a new player.

        Args:
            username (str): name of the player
            id (UUID): ID of the player
            response (bool): true if the player was created successfully, false otherwise

        Returns:
            Message: the constructed message
        """
        ...

    def create_new_lobby_message(self, player_id: UUID, lobby_id: int, response: bool) -> Message:
        """
        Create a message to create a new lobby.

        Args:
            player_id (UUID): ID of the player
            lobby_id (int): ID of the lobby
            response (bool): true if the lobby was created successfully, false otherwise

        Returns:
            Message: the constructed message
        """
        ...

    def create_ready_to_play_message(self,
                                     player_id: UUID,
                                     lobby_id: int,
                                     ready: bool,
                                     players_in_lobby: list[Player]
                                     ) -> Message:
        """
        Create a message to indicate that a player is ready to play.

        Args:
            player_id (UUID): player who is ready or not
            lobby_id (int): ID of the lobby
            ready (bool): true if the player is ready, false otherwise
            players_in_lobby (list[Player]): list of players in the lobby

        Returns:
            Message: the constructed message
        """
        ...

    def create_start_game_message(self, lobby_id: int) -> Message:
        """
        Create a message to start a game.

        Args:
            lobby_id (int): ID of the lobby

        Returns:
            Message: the constructed message
        """
        ...

    def create_join_lobby_message(self, player_id: UUID, lobby_id: int, players_in_lobby: list[Player], response: bool) -> Message:
        """
        Create a message to join a lobby.

        Args:
            player_id (UUID): ID of the player
            lobby_id (int): ID of the lobby
            players_in_lobby (list[Player]): list of players in the lobby
            response (bool): true if the player joined successfully, false otherwise

        Returns:
            Message: the constructed message
        """
        ...

    def create_leave_lobby_message(self, player_id: UUID, lobby_id: int) -> Message:
        """
        Create a message to leave a lobby.

        Args:
            player_id (UUID): ID of the player
            lobby_id (int): ID of the lobby

        Returns:
            Message: the constructed message
        """
        ...

    def create_remove_player_message(self, player_id: UUID) -> Message:
        """
        Create a message to remove a player.
        Args:
            player_id (UUID): ID of the player to remove
        Returns:
            Message: the constructed message
        """
        ...

    def create_heartbeat_message(self) -> Message:
        """
        Create a message to check if the server connection is alive.

        Returns:
            Message: the constructed message
        """

    def create_server_error_message(self) -> Message:
        """
        Create a message to indicate a server error.

        Returns:
            Message: the constructed message
        """
        ...
