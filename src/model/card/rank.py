from enum import Enum


class Rank(Enum):
    """
    Enum class that represents the possible ranks of cards in a poker game.
    Each rank is mapped to its numeric value.
    """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    def next(self):
        """
        Get the next rank in the sequence
        Returns:
            Rank: the next rank in the sequence, None if it's the highest
        """
        ranks = list(self.__class__)
        idx = ranks.index(self)
        return ranks[idx + 1] if idx + 1 < len(ranks) else None
    
    def previous(self):
        """
        Get the previous rank in the sequence
        Returns:
            Rank: the previous rank in the sequence, None if it's the lowest
        """
        ranks = list(self.__class__)
        idx = ranks.index(self)
        return ranks[idx - 1] if idx - 1 >= 0 else None
    
    def __str__(self):
        res = str(self.value)
        match self.value:
            case 11: res = "jack"
            case 12: res = "queen"
            case 13: res = "king"
            case 14: res = "ace"
        return res
