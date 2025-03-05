from enum import Enum


class Combination(Enum):
    """
    Enum class that represents the possible combinations of cards in a poker game.
    To each one is assigned a value that represents its importance in the game.
    """
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10
