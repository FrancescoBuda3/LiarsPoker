from dataclasses import dataclass
from uuid import UUID
from src.model.card import Card

@dataclass
class Player():
    id: UUID
    username: str
    cards: list[Card]
    cards_in_hand: int
    ready: bool

    def __init__(self, username:str, id: UUID):
        self.username = username
        self.id = id
        self.cards = []
        self.cards_in_hand = 0
        self.ready = False
    
    def __post_init__(self):
        if not self.username:
            raise ValueError("Username is required")
        if not self.id:
            raise ValueError("ID is required")
        
    def __str__(self):
        return f"Player({self.username}, {self.id})"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Player):
            return False
        return self.id == value.id