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

    def create_new_player_message(self, player: str, id: UUID) -> Message:
        return Message({
            "player": Player(player, id)
        })
        
    def create_new_lobby_message(self, player_id: UUID, lobby_id: int = 0) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id
        })

    def create_join_lobby_message(self, player_id: UUID, lobby_id: int, status: bool = True, players_in_lobby:list = []) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id,
            "status": status,
            "players_in_lobby": players_in_lobby
        })
        
    def create_new_game_message(self, lobby_id):
        return Message({
            "lobby_id": lobby_id
        })