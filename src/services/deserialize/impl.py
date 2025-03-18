from src.model.card import Card
from src.model.player import Player
from src.model.stake import Stake


class Deserializer:
    def deserialize(self, string):
        return self._ast_to_obj(self._string_to_ast(string))
        
    def _string_to_ast(self, string):
        ...
    
    def _ast_to_message(self, data):
        ...
    
    def _ast_to_obj(self, data):
        ...

    def _ast_to_player(self, data) -> Player:
        ...
    
    def _ast_to_card(self, data) -> Card:
        ...

    def _ast_to_stake(self, data) -> Stake:
        ...