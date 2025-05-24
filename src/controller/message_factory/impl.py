from uuid import UUID
from src.controller.message_factory import MessageFactoryInterface
from src.model.card import Card
from src.model.player import Player
from src.model.stake import Stake
from src.services.message import Message


class MessageFactory(MessageFactoryInterface):

    def create_start_turn_message(self, player: Player, minimum_stake: Stake) -> Message:
        return Message({
            "player": player,
            "minimum_stake": minimum_stake
        })

    def create_start_round_message(self, players: list[Player]) -> Message:
        return Message({
            "players": players
        })
    
    def create_game_info_message(self, interested_player:Player, players: list[Player] = [], turn_player: Player = None, latest_stake: Stake = None, min_next_stake: Stake = None) -> Message:
        return Message({
            "interested_player": interested_player,
            "players": players,
            "turn_player": turn_player,
            "latest_stake": latest_stake,
            "min_next_stake": min_next_stake
        })

    def create_round_loser_message(self, player: Player, cards: list[Card], elimination: bool) -> Message:
        return Message({
            "player": player,
            "cards": cards,
            "elimination": elimination
        })

    def create_game_over_message(self, player: Player) -> Message:
        return Message({
            "player": player
        })

    def create_raise_stake_message(self, player: Player, stake: Stake) -> Message:
        return Message({
            "player": player,
            "stake": stake
        })

    def create_check_liar_message(self) -> Message:
        return Message({})

    def create_new_player_message(self, username: str, id: UUID, response: bool = True) -> Message:
        return Message({
            "username": username,
            "player_id": id,
            "response": response
        })

    def create_new_lobby_message(self, player_id: UUID, lobby_id: int = 0, response: bool = True) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id,
            "response": response
        })

    def create_ready_to_play_message(self,
                                     player_id: UUID,
                                     lobby_id: int,
                                     ready: bool,
                                     players_in_lobby: list[Player] = []
                                     ) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id,
            "ready": ready,
            "players_in_lobby": players_in_lobby
        })

    def create_start_game_message(self, lobby_id: int) -> Message:
        return Message({
            "lobby_id": lobby_id
        })

    def create_join_lobby_message(self, player_id: UUID, lobby_id: int, players_in_lobby: list[Player] = [], response: bool = True) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id,
            "players_in_lobby": players_in_lobby,
            "response": response
        })

    def create_leave_lobby_message(self, player_id: UUID, lobby_id: int) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id
        })

    def create_remove_player_message(self, player_id: UUID) -> Message:
        return Message({
            "player_id": player_id
        })

    def create_heartbeat_message(self) -> Message:
        return Message({
            "status": "alive"
        })
        
    def create_server_error_message(self):
        return Message({
            "error": "Server error"
        })
