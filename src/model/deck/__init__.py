from dataclasses import dataclass
import random
from typing import List

from suit import Suit
from combination import Combination


@dataclass
class Card():
    suit: Suit
    rank: int


@dataclass
class Deck():
    cards: List[Card]

    def shuffle(self, hands: List[int]):
        """_summary_

        Args:
            hands (List[int]): list of number of cards to be distributed to each hand

        Returns:
            List[int]: list of hands with the number of cards specified in the input
        """
        random.shuffle(self.cards)
        retList = []
        for hand in hands:
            retList.append(self.cards[:hand])
            self.cards = self.cards[hand:]
        return retList


# generate a deck of cards with 52 cards
def generate_deck():
    deck = Deck([])
    for suit in Suit:
        for rank in range(1, 14):
            deck.cards.append(Card(suit, rank))
    return deck


print(generate_deck().shuffle([5, 5, 5]))


@dataclass
class Stake:
    ranks: List[int]
    combo: Combination
