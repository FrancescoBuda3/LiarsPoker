from enum import Enum
import json
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.services.message import Message

#class MessageType(Enum):
#    SART_GAME = "start_game"
#    START_ROUND = "start_round"
#    START_TURN = "start_turn"
#    ROUNT_LOSER = "round_loser"
#    SHOW_CARDS = "show_cards"
#    ELIMINATION = "elimination"
#    GAME_OVER = "game_over"

class Deserializer:
    def deserialize(self, string):
        return self._ast_to_obj(self._string_to_ast(string))
        
    def _string_to_ast(self, string):
        return json.loads(string)
    
    def _ast_to_obj(self, data):
        if isinstance(data, dict):
            if '$type' not in data:
                return {key: self._ast_to_obj(value) for key, value in data.items()}
            # selects the appropriate method to convert the AST to object via reflection
            method_name = f'_ast_to_{data["$type"].lower()}'
            if hasattr(self, method_name):
                return getattr(self, method_name)(data)
            raise ValueError(f"Unsupported type {data['type']}")
        if isinstance(data, list):
            return [self._ast_to_obj(item) for item in data]
        return data

    
    def _ast_to_message(self, data):
        return Message(
            header = self._ast_to_obj(data["header"]),
            body = self._ast_to_obj(data["body"])
        )
    
    def _ast_to_player(self, data) -> Player:
        return Player(
            username = data["username"],
        )
    
    def _ast_to_card(self, data) -> Card:
        return Card(
            rank = self._ast_to_obj(Rank.__members__[data["rank"]]),
            suit = self._ast_to_obj(Rank.__members__[data["suit"]])
        )

    def _ast_to_stake(self, data) -> Stake:
        return Stake(
            combo = self._ast_to_obj(Combination.__members__[data["combo"]]),
            ranks = self._list_to_enum(data["ranks"], Rank),
            suits = self._list_to_enum(data["suits"], Suit)
        )
        
    def _list_to_enum(self, data, enum):
        return [self._ast_to_obj(enum.__members__[item]) for item in data]