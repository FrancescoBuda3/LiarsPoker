from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from src.model.deck import Card

from .combination import Combination


@dataclass
class Stake:
    """
    Models the stake that a player calls when playing.
    
    A stake is a combination of cards and a list of ranks.
    """
    ranks: set[int]
    combo: Combination
    
class LowestStake(Enum):
    """
    Enum class that represents the possible lowest combinations of cards in a poker game.
    Each value is mapped to the lowest stake that represent the lowest combination.
    """
    HIGH_CARD = Stake([1], Combination.HIGH_CARD)
    PAIR = Stake([1], Combination.PAIR)
    TWO_PAIR = Stake([1, 1], Combination.TWO_PAIR)
    THREE_OF_A_KIND = Stake([1], Combination.THREE_OF_A_KIND)
    STRAIGHT = Stake([1, 2, 3, 4, 5], Combination.STRAIGHT)
    FLUSH = Stake([], Combination.FLUSH)
    FULL_HOUSE = Stake([1, 2], Combination.FULL_HOUSE)
    FOUR_OF_A_KIND = Stake([1], Combination.FOUR_OF_A_KIND)
    STRAIGHT_FLUSH = Stake([1, 2, 3, 4, 5], Combination.STRAIGHT_FLUSH)
    ROYAL_FLUSH = Stake([10, 11, 12, 13, 14], Combination.ROYAL_FLUSH)


class StakeHandler(Protocol):
        
    def reset_stake(self) -> None:
        """
        Resets the current stake.
        """
        ...

    def check_cards(self, cards: set[Card]) -> bool:
        """
        Checks if the given cards contain the valid combination for the current stake.
        Args:
            cards (set[Card]): the cards to check

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
        
    def check_raise(self, stake: Stake) -> bool:
        """
        Checks if the given stake is a valid raise.
        Args:
            stake (Stake): the stake to check

        Returns:
            bool: true if the stake is a valid raise, false otherwise
        """
        ...
