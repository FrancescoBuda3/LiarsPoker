from dataclasses import dataclass
from typing import List

from src.model.deck.suit import Suit


@dataclass
class Card():
    suit: Suit
    rank: int


@dataclass
class Deck():
    
    def shuffle(self, hands: List[int]):
        """_summary_

        Args:
            hands (List[int]): list of number of cards to be distributed to each hand

        Returns:
            List[int]: list of hands with the number of cards specified in the input
        """
        pass
