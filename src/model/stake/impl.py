from src.model.deck import Card
from ..stake import StakeHandler, Stake, Combination


class StakeHandlerImpl(StakeHandler):
    """
    The implementation of a simple helper class that models an object that
    keeps a called stake and checks if a given set of cards is valid for the stake.
    """
    _stake: Stake

    def __init__(self):
        self._stake = None

    def get_stake(self) -> Stake:
        if (self._stake == None):
            raise ValueError("No stake has been set")
        return self._stake

    def set_stake(self, stake: Stake) -> None:
        self._stake = stake

    def check_cards(self, cards: list[Card]) -> bool:
        card_ranks = [card.rank for card in cards]
        card_suits = [card.suit for card in cards]
        match self._stake.combo:
            case Combination.HIGH_CARD:
                return max(card_ranks) == self._stake.ranks[0]
            case Combination.PAIR:
                return card_ranks.count(self._stake.ranks[0]) >= 2
            case Combination.TWO_PAIR:
                return card_ranks.count(self._stake.ranks[0]) >= 2 and card_ranks.count(self._stake.ranks[1]) >= 2
            case Combination.THREE_OF_A_KIND:
                return card_ranks.count(self._stake.ranks[0]) >= 3
            case Combination.STRAIGHT:
                return self.__check_straight(card_ranks)
            case Combination.FLUSH:
                return max([card_suits.count(suit) for suit in card_suits]) >= 5
            case Combination.FULL_HOUSE:
                return card_ranks.count(self._stake.ranks[0]) >= 3 and card_ranks.count(self._stake.ranks[0]) >= 2
            case Combination.FOUR_OF_A_KIND:
                return card_ranks.count(self._stake.ranks[0]) >= 4
            case Combination.STRAIGHT_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                for suit in cards_by_suit:
                    if len(cards_by_suit[suit]) >= 5 and self.__check_straight(cards_by_suit[suit]):
                        return True
                return False
            case Combination.ROYAL_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                for suit in cards_by_suit:
                    if len(cards_by_suit[suit]) >= 5 and min(cards_by_suit[suit]) == 10 and max(cards_by_suit[suit]) == 14 and self.__check_straight(cards_by_suit[suit]):
                        return True
                return False
            case _:
                return False

    def __check_straight(self, ranks: list[int]) -> bool:
        ranks = sorted(set(ranks))
        for i in range(len(ranks) - 4):
            if all(ranks[i + j] == ranks[i] + j for j in range(5)):
                return True
        return False
    
    def __group_suits(self, cards: list[Card]) -> dict:
        cards_by_suit = {}
        for card in cards:
            if card.suit not in cards_by_suit:
                cards_by_suit[card.suit] = []
            cards_by_suit[card.suit].append(card.rank)
        return cards_by_suit
