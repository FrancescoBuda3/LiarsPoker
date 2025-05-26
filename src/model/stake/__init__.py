from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit

from .combination import Combination


@dataclass
class Stake:
    combo: Combination
    ranks: list[Rank]
    suits: list[Suit]
    
    def __init__(self, combo: Combination, ranks: list[Rank] = [], suits: list[Suit] = []):
        """
        Models the stake that a player calls when playing.
        Args:
            combo (Combination): the combination of the stake
            ranks (list[Rank], optional): the ranks of the cards in the stake. Defaults to empty.
            suits (list[Suit], optional): the suits of teh cards in the stake. Defaults to empty.
        """
        self.combo = combo
        self.ranks = ranks
        self.suits = suits
    
    def __post_init__(self):
        if not self.combo:
            raise ValueError("Combination is required")
        
    @property
    def single_rank(self) -> Rank:
        if len(self.ranks) == 0:
            raise ValueError("No rank has been set")
        return self.ranks[0]
    
    @single_rank.setter
    def single_rank(self, rank: Rank):
        self.ranks = [rank]
    
    @property
    def pair_rank(self) -> Rank:
        if len(self.ranks) == 0:
            raise ValueError("No rank has been set")
        if len(self.ranks) == 1:
            return self.ranks[0]
        return self.ranks[1]
    
    @pair_rank.setter
    def pair_rank(self, rank: Rank):
        if len(self.ranks) >= 1:
            self.ranks = [self.ranks[0], rank]
        else:
            self.ranks = [rank]
    
    @property
    def triple_rank(self) -> Rank:
        if len(self.ranks) == 0:
            raise ValueError("No rank has been set")
        return self.ranks[0]
    
    @triple_rank.setter
    def triple_rank(self, rank: Rank):
        if len(self.ranks) >= 1:
            self.ranks = [rank, self.ranks[0]]
        else:
            self.ranks = [rank]
        
    @property
    def suit(self) -> Suit:
        if len(self.suits) == 0:
            raise ValueError("No suit has been set")
        return self.suits[0]
    
    @suit.setter
    def suit(self, suit: Suit):
        self.suits = [suit]
    
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


class StakeHandlerInterface(Protocol):
        
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
        
    def get_lowest_next_stake(self) -> Stake | None:
        """
        Returns the lowest possible stake that can be called.
        If the stake can't be raised higher than None is returned.
        Returns:
            Stake: the lowest stake
        """
        ...
