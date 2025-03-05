from dataclasses import dataclass
from typing import Protocol

from src.model.deck import Card

from .combination import Combination


@dataclass
class Stake:
    """
    Models the stake that a player calls when playing.
    
    A stake is a combination of cards and a list of ranks.
    """
    ranks: list[int]
    combo: Combination


class StakeHandler(Protocol):
    def get_stake(self) -> Stake:
        """
        Returns the current stake, if not set raises an error.
        Returns:
            Stake: the current stake
        """
        ...
    
    def set_stake(self, stake: Stake) -> None:
        """
        Sets the given stake as the current stake.
        Args:
            stake (Stake): a stake called by a player
        """
        ...

    def check_cards(self, cards: list[Card]) -> bool:
        """
        Checks if the given cards are valid for the current stake.
        Args:
            cards (list[Card]): the cards to check

        Returns:
            bool: true if the cards are valid, false otherwise
        """
        ...
