from dataclasses import dataclass
import random

from src.model.deck import Deck, Card
from src.model.deck.suit import Suit


@dataclass
class DeckImpl(Deck):
    
    cards: list[Card]
    
    def __init__(self):
        self.cards = self.__generate_deck()
    
    def shuffle(self, hands: list[int]):
        random.shuffle(self.cards)
        retList = []
        for hand in hands:
            retList.append(self.cards[:hand])
            self.cards = self.cards[hand:]
        return retList
    
    def __generate_deck(self):
        retList = []
        for suit in Suit:
            for rank in range(1, 14):
                retList.append(Card(suit, rank))
        return retList