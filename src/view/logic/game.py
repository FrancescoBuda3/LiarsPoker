from src.model.card import Card
from src.model.card.rank import Rank
from src.model.stake.combination import Combination


def check_cards_combination(cards: list[Card], combo: Combination) -> bool:
    if len(cards) > 0:
        match combo:
            case Combination.STRAIGHT:
                cards.sort(key=lambda x: x.rank.value)
                return all(
                    cards[i].rank.value == cards[i + 1].rank.value - 1
                    for i in range(len(cards) - 1)
                )
            case Combination.STRAIGHT_FLUSH: 
                cards.sort(key=lambda x: x.rank.value)
                return all(
                    cards[i].suit == cards[i + 1].suit
                    for i in range(len(cards) - 1)
                ) and all(
                    cards[i].rank.value == cards[i + 1].rank.value - 1
                    for i in range(len(cards) - 1)
                )
            case _:
                return True
    return False
