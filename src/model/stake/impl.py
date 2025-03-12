from src.model.deck import Card
from src.model.deck.suit import Suit
from ..stake import LowestStake, StakeHandler, Stake, Combination


class _SuitsHandler:
    """
    A simple helper class that models an object that keeps track of the suits 
    that have been used in the current flush stake.
    """
    suits: set[Suit]
    combo: Combination

    def __init__(self):
        self.suits = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]
        self.combo = None

    @property
    def flush_combos(self) -> set[Combination]:
        return [Combination.FLUSH, Combination.STRAIGHT_FLUSH, Combination.ROYAL_FLUSH]


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
                if len(cards_by_suit[self.stake.suit]) >= 5 and self.__check_straight(cards_by_suit[self.stake.suit]):
                    check = True
            case Combination.ROYAL_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                if len(cards_by_suit[self.stake.suit]) >= 5 and min(cards_by_suit[self.stake.suit]) == 10 and + \
                        max(cards_by_suit[self.stake.suit]) == 14 and self.__check_straight(cards_by_suit[self.stake.suit]):
                    check = True
        return check

    def __check_straight(self, ranks: set[int]) -> bool:
        ranks = sorted(set(ranks))
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
            lowest_next_stake = None
            for stake in LowestStake:
                if stake.value.combo.value == current_combo.value+1:
                    lowest_next_stake = stake
            match current_combo:
                case Combination.HIGH_CARD | Combination.PAIR | Combination.THREE_OF_A_KIND | Combination.FOUR_OF_A_KIND:
                    lowest_stake = Stake(
                        current_combo, [self.stake.ranks[0]+1])
                    lowest_stake = lowest_stake if self.stake.ranks[0] + \
                        1 <= 14 else lowest_next_stake
                case Combination.TWO_PAIR:
                    biggest_value = max(self.stake.ranks)
                    lowest_value = min(self.stake.ranks)
                    lowest_stake = Stake(
                        current_combo, [biggest_value, lowest_value+1])
                    lowest_stake = lowest_stake if lowest_value+1 <= 14 else lowest_next_stake
                case Combination.STRAIGHT | Combination.STRAIGHT_FLUSH:
                    biggest_value = max(self.stake.ranks)
                    lowest_value = min(self.stake.ranks)
                    if len(self.__suits_handler.suits) <= 0:
                        biggest_value = biggest_value+1
                        lowest_value = lowest_value+1
                    ranks = [i for i in range(lowest_value, biggest_value+1)]
                    lowest_stake = Stake(current_combo, ranks, self.__suits_handler.suits)
                    lowest_stake = lowest_stake if biggest_value <= 14 else lowest_next_stake
                case Combination.FLUSH | Combination.ROYAL_FLUSH:
                    if len(self.__suits_handler.suits) > 0:
                        lowest_stake = Stake(
                            current_combo, suits=self.__suits_handler.suits)
                    else:
                        lowest_stake = lowest_next_stake
                case Combination.FULL_HOUSE:
                    tris = self.stake.ranks[0]
                    bis = self.stake.ranks[1]
                    if bis < tris:
                        bis = bis + 2
                        lowest_stake = Stake(current_combo, [tris, bis])
                        lowest_stake = lowest_stake if bis <= 13 else lowest_next_stake
                    else:
                        tris = tris + 1
                        bis = bis - 1
                        lowest_stake = Stake(current_combo, [tris, bis])
                        lowest_stake = lowest_stake if tris <= 14 else lowest_next_stake
        return lowest_stake
