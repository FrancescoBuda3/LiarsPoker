from uuid import UUID
from src.controller.message_factory import MessageFactoryInterface
from src.model.card import Card
from src.model.player import Player
from src.model.stake import Stake
from src.services.message import Message


class MessageFactory(MessageFactoryInterface):

    def create_show_cards_message(self, cards: list[Card]) -> Message:
        return Message({
            "cards": cards
        })

    def create_start_turn_message(self, player: Player, minimum_stake: Stake) -> Message:
        return Message({
            "player": player,
            "minimum_stake": minimum_stake
        })

    def create_start_round_message(self, players: list[Player]) -> Message:
        return Message({
            "players": players
        })

    def create_round_loser_message(self, player: Player) -> Message:
        return Message({
            "player": player
        })

    def create_elimination_message(self, player: Player) -> Message:
        return Message({
            "player": player
        })

    def create_game_over_message(self, player: Player) -> Message:
        return Message({
            "player": player
        })

    def create_raise_stake_message(self, stake: Stake) -> Message:
        return Message({
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

    def create_join_lobby_message(self, player_id: UUID, lobby_id: int) -> Message:
        return Message({
            "player_id": player_id,
            "lobby_id": lobby_id
        })