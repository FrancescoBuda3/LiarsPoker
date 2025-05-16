import json

from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.services.message import Message
from src.services.serialize import SeriliazerInterface


class Serializer(SeriliazerInterface):

    def serialize(self, obj):
        return self._ast_to_string(self._to_ast(obj))

    def _ast_to_string(self, data):
        return json.dumps(data, indent=2)

    def _to_ast(self, obj):
        if isinstance(obj, self._primitive_types):
            return obj
        if isinstance(obj, self._container_types):
            return [self._to_ast(item) for item in obj]
        if isinstance(obj, dict):
            return {key: self._to_ast(value) for key, value in obj.items()}
        # selects the appropriate method to convert the object to AST via reflection
        method_name = f'_{type(obj).__name__.lower()}_to_ast'
        if hasattr(self, method_name):
            data = getattr(self, method_name)(obj)
            data['$type'] = type(obj).__name__
            return data
        raise ValueError(f"Unsupported type {type(obj)}")
    
    def _message_to_ast(self, request: Message):
        return {
            'body': self._to_ast(request.body),
        }

    def _player_to_ast(self, player: Player):
        return {
            'username': self._to_ast(player.username),
            'id': self._to_ast(player.id),
            'cards': [self._to_ast(card) for card in player.cards],
            'cards_in_hand': self._to_ast(player.cards_in_hand),
            'ready': self._to_ast(player.ready),
        }
        
    def _uuid_to_ast(self, uuid):
        return {
            'id': str(uuid),
        }

    def _card_to_ast(self, card: Card):
        return {
            'suit': self._to_ast(card.suit),
            'rank': self._to_ast(card.rank),
        }
        
    def _suit_to_ast(self, suit: Suit):
        return {'name': suit.name}
    
    def _rank_to_ast(self, rank: Rank):
        return {'name': rank.name}
    
    def _stake_to_ast(self, stake: Stake):
        return {
            'ranks': [self._to_ast(rank) for rank in stake.ranks],
            'suits': [self._to_ast(suit) for suit in stake.suits],
            'combo': self._to_ast(stake.combo),
        }
        
    def _combination_to_ast(self, combination: Combination):
        return {'name': combination.name}
