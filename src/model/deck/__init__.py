from dataclasses import dataclass

from src.model.deck.suit import Suit


@dataclass
class Card():
    suit: Suit
    rank: int


class Deck():
    
    def shuffle(self, hands: list[int]):
        """
        Args:
            hands (list[int]): list of number of cards to be distributed to each hand

        Returns:
            list[int]: list of hands with the number of cards specified in the input
        """
        pass

@dataclass
class Stake:
    ranks: list[int]
    combo: Combination
