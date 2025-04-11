from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit

from .combination import Combination


@dataclass
class Stake:
    ranks: list[Rank]
    suits: set[Suit]
    combo: Combination
    
    def __init__(self, combo: Combination, ranks: list[Rank] = None, suits = None):
        """
        Models the stake that a player calls when playing.
        Args:
            combo (Combination): the combination of the stake
            ranks (list[Rank], optional): the ranks of the cards in the stake. Defaults to None.
            suits (Suit or set[Suit], optional): the suit or suits of the stake. Defaults to None.
        """
        self.combo = combo
        self.ranks = ranks if ranks is not None else set()
        if suits is None:
            self.suits = set()
        elif isinstance(suits, Suit):
            self.suits = {suits}
        else:
            self.suits = set(suits)
    
    def __post_init__(self):
        if not self.combo:
            raise ValueError("Combination is required")
        
    @property
    def suit(self) -> Suit:
        return next(iter(self.suits), None)
    
    @suit.setter
    def suit(self, suit: Suit):
        self.suits = {suit}
    
class LowestStake(Enum):
    """
    Enum class that represents the possible lowest combinations of cards in a poker game.
    Each value is mapped to the lowest stake that represent the lowest combination.
    """
    HIGH_CARD = Stake(Combination.HIGH_CARD, [Rank.ONE])
    PAIR = Stake(Combination.PAIR, [Rank.ONE])
    TWO_PAIR = Stake(Combination.TWO_PAIR, [Rank.ONE, Rank.ONE])
    THREE_OF_A_KIND = Stake(Combination.THREE_OF_A_KIND, [Rank.ONE])
    STRAIGHT = Stake(Combination.STRAIGHT, [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE])
    FLUSH = Stake(Combination.FLUSH)
    FULL_HOUSE = Stake(Combination.FULL_HOUSE, [Rank.ONE, Rank.TWO])
    FOUR_OF_A_KIND = Stake(Combination.FOUR_OF_A_KIND, [Rank.ONE])
    STRAIGHT_FLUSH = Stake(Combination.STRAIGHT_FLUSH, [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE])
    ROYAL_FLUSH = Stake(Combination.ROYAL_FLUSH, [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE])


class StakeHandler(Protocol):
        
    def reset_stake(self) -> None:
        """
        Resets the current stake.
        """
        ...

    def check_cards(self, cards: list[Card]) -> bool:
        """
        Checks if the given cards contain the valid combination for the current stake.
        Args:
            cards (list[Card]): the cards to check

        Returns:
            bool: true if the cards are valid, false otherwise
        """
        ...
        
    def get_lowest_next_stake(self) -> Stake:
        """
        Returns the lowest possible stake that can be called.
        If the stake can't be raised higher than None is returned.
        Returns:
            Stake: the lowest stake
        """
        ...
