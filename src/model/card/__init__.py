from dataclasses import dataclass

from src.model.card.rank import Rank
from src.model.card.suit import Suit


@dataclass(frozen=True)
class Card():
    suit: Suit
    rank: Rank
