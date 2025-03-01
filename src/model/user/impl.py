from model.deck import Card
from ..user import *

class Player(User):
    _cards: list[Card]
    
    def __init__(self, username: str, address: tuple[str, int]):
        super().__init__(username, address)
        
    @property
    def cards(self) -> list[Card]:
        return self._cards
    
    @cards.setter
    def cards(self, cards: list[Card]):
        self._cards = cards 