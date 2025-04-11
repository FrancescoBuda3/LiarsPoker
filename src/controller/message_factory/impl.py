from src.controller.message_factory import MessageFactoryInterface
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import Stake
from src.services.message import Header, Message
from src.services.serialize.impl import Serializer


class MessageFactory(MessageFactoryInterface):
    def __init__(self):
        self._serializer = Serializer()

    def create_show_cards_message(self, cards: list[Card]) -> str:
        return self._serializer.serialize(Message(Header.SHOW_CARDS, cards))
    
    def create_start_turn_message(self, player: Player, minimum_stake: Stake) -> str:
        return self._serializer.serialize(Message(Header.START_TURN, {
            "player": player,
            "minimum_stake": minimum_stake
        }))
        
    def create_start_round_message(self, players: list[Player]) -> str:
        return self._serializer(Message(Header.START_ROUND, players))
    
    def create_round_loser_message(self, player: Player) -> str:
        return self._serializer.serialize(Message(Header.ROUND_LOSER, player))
    
    def create_elimination_message(self, player: Player) -> str:
        return self._serializer.serialize(Message(Header.ELIMINATION, player))
    
    def create_game_over_message(self, player: Player) -> str:
        return self._serializer.serialize(Message(Header.GAME_OVER, player))
    
    def create_raise_stake_message(self, stake: Stake) -> str:
        return self._serializer.serialize(Message(Header.RAISE_STAKE, stake))
    
    def create_check_liar_message(self) -> str:
        return self._serializer.serialize(Message(Header.CHECK_LIAR, None))
    