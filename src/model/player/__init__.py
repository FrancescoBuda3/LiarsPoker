from dataclasses import dataclass, field
from src.model.deck import Card

@dataclass
class Player():
    username: str
    cards: set[Card]
    cards_in_hand: int

    def __init__(self, username:str):
        self.username = username
        self.cards = []
        self.cards_in_hand = 0
    
    def __post_init__(self):
        if not self.username:
            raise ValueError("Username is required")