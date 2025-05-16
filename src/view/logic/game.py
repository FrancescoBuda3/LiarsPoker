from src.model.card import Card
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

def cards_permitted(combo: Combination) -> int:
    max_cards = 5
    match combo:
        case (
            Combination.HIGH_CARD
            | Combination.PAIR
            | Combination.THREE_OF_A_KIND
            | Combination.FOUR_OF_A_KIND
        ):
            max_cards = 1
        case (
            Combination.TWO_PAIR
            | Combination.FULL_HOUSE
        ):
            max_cards = 2
    return max_cards
