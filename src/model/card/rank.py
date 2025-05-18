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
    
    def next(self, steps = 1):
        """
        Get the next rank in the sequence
        Args:
            steps (int): number of steps to move forward in the sequence
        Returns:
            Rank: the next rank in the sequence, None if it's the highest
        """
        ranks = list(self.__class__)
        idx = ranks.index(self)
        return ranks[idx + steps] if idx + steps < len(ranks) else None
    
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
        return str(self.value)
    
    def to_symbol(self):
        """
        Convert the rank to its symbol representation.
        Returns:
            str: the symbol representation of the rank
        """
        if self == Rank.JACK:
            return 'Jack'
        elif self == Rank.QUEEN:
            return 'Queen'
        elif self == Rank.KING:
            return 'King'
        elif self == Rank.ACE:
            return 'Ace'
        else:
            return str(self.value)
