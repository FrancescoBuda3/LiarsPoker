from dataclasses import dataclass
from uuid import UUID
from src.model.card import Card

@dataclass
class Player():
    id: UUID
    username: str
    cards: list[Card]
    cards_in_hand: int

    def __init__(self, username:str, id: UUID):
        self.username = username
        self.id = id
        self.cards = []
        self.cards_in_hand = 0
    
    def __post_init__(self):
        if not self.username:
            raise ValueError("Username is required")
        if not self.id:
            raise ValueError("ID is required")
        
    def __str__(self):
        return f"Player({self.username}, {self.id})"