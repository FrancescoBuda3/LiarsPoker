from enum import Enum


class Suit(Enum):
    """
    Enum class that represents the possible suits of cards in a poker game.
    Each suit it's mapped to its string representation.
    """
    SPADES = "spades"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"

    def __str__(self):
        return self.value
