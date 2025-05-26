import random

from src.model.card.rank import Rank
from src.model.deck import DeckInterface
from src.model.card import Card
from src.model.card.suit import Suit


class Deck(DeckInterface):
    
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
            for rank in range(Rank.ONE.value, Rank.ACE.value):
                retList.append(Card(suit, Rank(rank)))
        return retList