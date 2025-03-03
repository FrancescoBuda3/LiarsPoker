from dataclasses import dataclass
from model.deck import Card

@dataclass
class Player():
    username: str
    cards: list[Card]
    cardsInHand: int
    
    def __post_init__(self):
        if not self.username:
            raise ValueError("Username is required")