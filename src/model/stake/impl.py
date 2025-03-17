from src.model.card import *
from src.model.card.suit import Suit
from ..stake import *


class _SuitsHandler:
    """
    A simple helper class that models an object that keeps track of the suits
    that have been used in the current flush stake.
    """
    suits: set[Suit]
    combo: Combination

    def __init__(self):
        self.suits = {Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS}
        self.combo = None

    @property
    def flush_combos(self) -> set[Combination]:
        return {Combination.FLUSH, Combination.STRAIGHT_FLUSH, Combination.ROYAL_FLUSH}


class StakeHandlerImpl(StakeHandler):
    """
    The implementation of a simple helper class that models an object that
    keeps a called stake and checks if a given set of cards is valid for the stake.
    """

    def __init__(self):
        self._stake = None
        self.__suits_handler = _SuitsHandler()

    @property
    def stake(self) -> Stake:
        """
        Returns the current stake, if not set raises an error.
        Returns:
            Stake: the current stake
        """
        if (self._stake == None):
            raise ValueError("No stake has been set")
        return self._stake

    @stake.setter
    def stake(self, stake: Stake) -> None:
        """
        Sets the given stake as the current stake.
        Args:
            stake (Stake): a stake called by a player
        """
        self._stake = stake
        if self.__suits_handler.combo == None or self.__suits_handler.combo == stake.combo:
            self.__suits_handler.combo = stake.combo
            if stake.suit in self.__suits_handler.suits:
                self.__suits_handler.suits.remove(stake.suit)
        elif stake.combo in self.__suits_handler.flush_combos:
            self.__suits_handler = _SuitsHandler()
            self.__suits_handler.combo = stake.combo

    def reset_stake(self) -> None:
        self._stake = None
        self.__suits_handler = _SuitsHandler()

    def check_cards(self, cards: set[Card]) -> bool:
        card_ranks = [card.rank for card in cards]
        card_suits = [card.suit for card in cards]
        check = False
        match self.stake.combo:
            case Combination.HIGH_CARD:
                check = self.stake.ranks[0] in card_ranks
            case Combination.PAIR:
                check = card_ranks.count(self.stake.ranks[0]) >= 2
            case Combination.TWO_PAIR:
                check = card_ranks.count(self.stake.ranks[0]) >= 2 and card_ranks.count(
                    self.stake.ranks[1]) >= 2
            case Combination.THREE_OF_A_KIND:
                check = card_ranks.count(self.stake.ranks[0]) >= 3
            case Combination.STRAIGHT:
                check = self.__check_straight(card_ranks)
            case Combination.FLUSH:
                check = card_suits.count(self.stake.suit) >= 5
            case Combination.FULL_HOUSE:
                check = card_ranks.count(self.stake.ranks[0]) >= 3 and card_ranks.count(
                    self.stake.ranks[0]) >= 2
            case Combination.FOUR_OF_A_KIND:
                check = card_ranks.count(self.stake.ranks[0]) >= 4
            case Combination.STRAIGHT_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                check = len(cards_by_suit[self.stake.suit]) >= 5 and self.__check_straight(
                    cards_by_suit[self.stake.suit])
            case Combination.ROYAL_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                cards = cards_by_suit[self.stake.suit]
                has_five_or_more = len(cards) >= 5
                min_rank = min(cards, key=lambda r: r.value)
                max_rank = max(cards, key=lambda r: r.value)
                is_min_ten = min_rank == Rank.TEN
                is_max_ace = max_rank == Rank.ACE
                is_straight = self.__check_straight(cards)
                check = has_five_or_more and is_min_ten and is_max_ace and is_straight
        return check

    def __check_straight(self, ranks: set[Rank]) -> bool:
        ranks = sorted([rank.value for rank in ranks])
        for i in range(len(ranks) - 4):
            if all(ranks[i + j] == ranks[i] + j for j in range(5)):
                return True
        return False

    def __group_suits(self, cards: set[Card]) -> dict:
        cards_by_suit = {}
        for card in cards:
            if card.suit not in cards_by_suit:
                cards_by_suit[card.suit] = []
            cards_by_suit[card.suit].append(card.rank)
        return cards_by_suit

    def get_lowest_next_stake(self) -> Stake:
        lowest_stake = LowestStake.HIGH_CARD
        if self._stake != None:
            current_combo = self.stake.combo
            max_rank = max(self.stake.ranks, key=lambda r: r.value) if len(
                self.stake.ranks) > 0 else None
            min_rank = min(self.stake.ranks, key=lambda r: r.value) if len(
                self.stake.ranks) > 0 else None
            lowest_next_stake = None
            for stake in LowestStake:
                if stake.value.combo == current_combo.next():
                    lowest_next_stake = stake
            match current_combo:
                case (
                    Combination.HIGH_CARD
                    | Combination.PAIR
                    | Combination.THREE_OF_A_KIND
                    | Combination.FOUR_OF_A_KIND
                ):
                    lowest_stake = Stake(
                        current_combo, [self.stake.ranks[0].next()])
                    lowest_stake = lowest_stake if self.stake.ranks[0].next(
                    ) else lowest_next_stake
                case Combination.TWO_PAIR:
                    lowest_stake = Stake(
                        current_combo, [max_rank, min_rank.next()])
                    lowest_stake = lowest_stake if min_rank else lowest_next_stake
                case Combination.STRAIGHT | Combination.STRAIGHT_FLUSH:
                    if len(self.__suits_handler.suits) <= 0:
                        max_rank = max_rank.next()
                        min_rank = min_rank.next()
                    ranks = [min_rank]
                    for i in range(max_rank.value - min_rank.value):
                        ranks.append(ranks[i].next())
                    lowest_stake = Stake(
                        current_combo, ranks, self.__suits_handler.suits)
                    lowest_stake = lowest_stake if max_rank else lowest_next_stake
                case Combination.FLUSH | Combination.ROYAL_FLUSH:
                    if len(self.__suits_handler.suits) > 0:
                        lowest_stake = Stake(
                            current_combo, suits=self.__suits_handler.suits)
                    else:
                        lowest_stake = lowest_next_stake
                case Combination.FULL_HOUSE:
                    tris = self.stake.ranks[0]
                    bis = self.stake.ranks[1]
                    if bis.value < tris.value:
                        bis = bis.next().next()
                        lowest_stake = Stake(current_combo, [tris, bis])
                        lowest_stake = lowest_stake if bis else lowest_next_stake
                    else:
                        tris = tris.next()
                        bis = bis.previous()
                        lowest_stake = Stake(current_combo, [tris, bis])
                        lowest_stake = lowest_stake if tris else lowest_next_stake
        return lowest_stake
