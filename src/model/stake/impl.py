from src.model.card import *
from src.model.card.suit import Suit
from ..stake import *

class _SuitsHandler:
    """
    A simple helper class that models an object that keeps track of the suits
    that have been used in the current flush stake.
    """
    suits: list[Suit]
    _combo: Combination | None
    __flush_combos: list[Combination] = [
        Combination.FLUSH, Combination.STRAIGHT_FLUSH, Combination.ROYAL_FLUSH]
    __strict_flush_combos: list[Combination] = [
        Combination.FLUSH, Combination.ROYAL_FLUSH]

    def __init__(self):
        self.__reset()
            
    def new_stake(self, stake: Stake):
        if stake.combo in self.__flush_combos:
            if self._combo == None or self._combo == stake.combo:
                self._combo = stake.combo
                if stake.combo in self.__strict_flush_combos:
                    if stake.suit in self.suits:
                        self.suits.remove(stake.suit)
                else:
                    max_rank = max(stake.ranks, key=lambda r: r.value)
                    max_rank = max_rank.next()
                    if not max_rank:
                        self.suits.remove(stake.suit)
            else:
                self.__reset()
            
    def __reset(self):
        self.suits = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
        self._combo = None


class StakeHandlerImpl(StakeHandler):
    """
    The implementation of a simple helper class that models an object that
    keeps a called stake and checks if a given set of cards is valid for the stake.
    """
    _stake: Stake | None
    __suits_handler: _SuitsHandler

    def __init__(self):
        self._stake = None
        self.__suits_handler = _SuitsHandler()

    @property
    def stake(self) -> Stake | None:
        """
        Returns the current stake or None.
        Returns:
            Stake: the current stake
        """
        return self._stake

    @stake.setter
    def stake(self, stake: Stake):
        """
        Sets the given stake as the current stake.
        Args:
            stake (Stake): a stake called by a player
        """
        self._stake = stake
        self.__suits_handler.new_stake(stake)

    def reset_stake(self):
        self._stake = None
        self.__suits_handler = _SuitsHandler()

    def check_cards(self, cards: list[Card]) -> bool:
        if self.stake is None:
            raise ValueError("Stake is not set. Cannot check cards.")
        cards = self.__double_ones_and_aces(cards)
        card_ranks: list[Rank] = [card.rank for card in cards]
        card_suits: list[Suit] = [card.suit for card in cards]
        check: bool = False
        match self.stake.combo:
            case Combination.HIGH_CARD:
                check = card_ranks.count(self.stake.single_rank) >= 1
            case Combination.PAIR:
                check = card_ranks.count(self.stake.single_rank) >= 2
            case Combination.TWO_PAIR:
                check = (card_ranks.count(self.stake.ranks[0]) >= 2
                    and card_ranks.count(self.stake.ranks[1]) >= 2)
            case Combination.THREE_OF_A_KIND:
                check = card_ranks.count(self.stake.single_rank) >= 3
            case Combination.STRAIGHT:
                check = self.__check_straight(card_ranks)
            case Combination.FLUSH:
                check = card_suits.count(self.stake.suit) >= 5
            case Combination.FULL_HOUSE:
                check = (card_ranks.count(self.stake.triple_rank) >= 3 
                    and card_ranks.count(self.stake.pair_rank) >= 2)
            case Combination.FOUR_OF_A_KIND:
                check = card_ranks.count(self.stake.single_rank) >= 4
            case Combination.STRAIGHT_FLUSH:
                cards_by_suit = self.__group_by_suit(cards)
                if self.stake.suit in cards_by_suit:
                    check = (len(cards_by_suit[self.stake.suit]) >= 5 
                            and self.__check_straight(cards_by_suit[self.stake.suit]))
            case Combination.ROYAL_FLUSH:
                cards_by_suit = self.__group_by_suit(cards)
                if self.stake.suit in cards_by_suit:
                    suit_ranks = cards_by_suit[self.stake.suit]
                    has_five_or_more = len(suit_ranks) >= 5
                    min_rank = min(suit_ranks, key=lambda r: r.value)
                    max_rank = max(suit_ranks, key=lambda r: r.value)
                    is_min_ten = min_rank == Rank.TEN
                    is_max_ace = max_rank == Rank.ACE
                    is_straight = self.__check_straight(suit_ranks)
                    check = has_five_or_more and is_min_ten and is_max_ace and is_straight
        return check

    def __double_ones_and_aces(self, cards: list[Card]) -> list[Card]:
        ones = [card for card in cards if card.rank == Rank.ONE]
        ones_suits = [card.suit for card in ones]
        aces = [card for card in cards if card.rank == Rank.ACE]
        aces_suits = [card.suit for card in aces]
        add_list = []
        for one in ones:
            if aces_suits.count(one.suit) == 0:
                add_list.append(Card(one.suit, Rank.ACE))
        for ace in aces:
            if ones_suits.count(ace.suit) == 0:
                add_list.append(Card(ace.suit, Rank.ONE))
        return cards + add_list

    def __check_straight(self, ranks: list[Rank]) -> bool:
        ranks = sorted(ranks, key=lambda r: r.value)
        for i in range(len(ranks) - 4):
            if all(ranks[i + j].value == ranks[i].value + j for j in range(5)):
                return True
        return False

    def __group_by_suit(self, cards: list[Card]) -> dict[Suit, list[Rank]]:
        cards_by_suit: dict[Suit, list[Rank]] = {}
        for card in cards:
            if card.suit not in cards_by_suit:
                cards_by_suit[card.suit] = []
            cards_by_suit[card.suit].append(card.rank)
        return cards_by_suit

    def get_lowest_next_stake(self) -> Stake | None:
        lowest_stake: Stake | None = LowestStake.HIGH_CARD.value
        if self._stake == None:
            return lowest_stake
        current_combo: Combination = self.stake.combo
        max_rank: Rank | None = None
        min_rank: Rank | None = None
        if len(self.stake.ranks) > 0:
            max_rank = max(self.stake.ranks, key=lambda r: r.value)
            min_rank = min(self.stake.ranks, key=lambda r: r.value)
        lowest_next_stake: Stake | None = None
        for low_stake in LowestStake:
            if low_stake.value.combo == current_combo.next():
                lowest_next_stake = low_stake.value
        lowest_stake = lowest_next_stake
        match current_combo:
            case (
                Combination.HIGH_CARD
                | Combination.PAIR
                | Combination.THREE_OF_A_KIND
                | Combination.FOUR_OF_A_KIND
            ):
                next_rank = self.stake.single_rank.next()
                if next_rank:
                    lowest_stake = Stake(current_combo, [next_rank])
            case Combination.TWO_PAIR:
                if min_rank and max_rank:
                    next_rank = min_rank.next()
                    if next_rank:
                        lowest_stake = Stake(current_combo, [max_rank, next_rank])
            case Combination.STRAIGHT:
                if max_rank and min_rank:
                    max_rank = max_rank.next()
                    min_rank = min_rank.next()
                    if max_rank and min_rank:
                        next_ranks: list[Rank] = [min_rank]
                        for i in range(max_rank.value - min_rank.value):
                            nxt_rk = next_ranks[i].next()
                            if nxt_rk:
                                next_ranks.append(nxt_rk)
                        lowest_stake = Stake(current_combo, next_ranks)
            case Combination.STRAIGHT_FLUSH:
                if min_rank and max_rank:
                    max_rank = max_rank.next()
                    min_rank = min_rank.next()
                    if max_rank and min_rank:
                        next_ranks: list[Rank] = [min_rank]
                        for i in range(max_rank.value - min_rank.value):
                            nxt_rk = next_ranks[i].next()
                            if nxt_rk:
                                next_ranks.append(nxt_rk)
                        lowest_stake = Stake(current_combo, next_ranks, self.__suits_handler.suits)
                    elif len(self.__suits_handler.suits) > 0:
                        lowest_stake = Stake(current_combo, self.stake.ranks, self.__suits_handler.suits) 
            case Combination.FLUSH | Combination.ROYAL_FLUSH:
                if len(self.__suits_handler.suits) > 0:
                    lowest_stake = Stake(current_combo, suits=self.__suits_handler.suits)
            case Combination.FULL_HOUSE:
                tris = self.stake.triple_rank
                bis = self.stake.pair_rank
                difference: int = tris.value - bis.value
                if difference == 1:
                    bis = bis.next(2)
                elif difference == -1:
                    tris = tris.next(2)
                elif difference > 0:
                    bis = bis.next()
                elif difference < 0:
                    tris = tris.next()
                if tris and bis:
                    lowest_stake = Stake(current_combo)
                    lowest_stake.triple_rank = tris
                    lowest_stake.pair_rank = bis
        return lowest_stake
