from src.model.deck import Card
from ..stake import LowestStake, StakeHandler, Stake, Combination


class StakeHandlerImpl(StakeHandler):
    """
    The implementation of a simple helper class that models an object that
    keeps a called stake and checks if a given set of cards is valid for the stake.
    """
    def __init__(self):
        self._stake = None
    
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
        
    def reset_stake(self) -> None:
        self._stake = None

    def check_cards(self, cards: set[Card]) -> bool:
        card_ranks = [card.rank for card in cards]
        card_suits = [card.suit for card in cards]
        check = False
        match self.stake.combo:
            case Combination.HIGH_CARD:
                check = card_ranks.count(self.stake.ranks[0]) >= 1
            case Combination.PAIR:
                check = card_ranks.count(self.stake.ranks[0]) >= 2
            case Combination.TWO_PAIR:
                check = card_ranks.count(self.stake.ranks[0]) >= 2 and card_ranks.count(self.stake.ranks[1]) >= 2
            case Combination.THREE_OF_A_KIND:
                check = card_ranks.count(self.stake.ranks[0]) >= 3
            case Combination.STRAIGHT:
                check = self.__check_straight(card_ranks)
            case Combination.FLUSH:
                check = max([card_suits.count(suit) for suit in card_suits]) >= 5
            case Combination.FULL_HOUSE:
                check = card_ranks.count(self.stake.ranks[0]) >= 3 and card_ranks.count(self.stake.ranks[0]) >= 2
            case Combination.FOUR_OF_A_KIND:
                check = card_ranks.count(self.stake.ranks[0]) >= 4
            case Combination.STRAIGHT_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                for suit in cards_by_suit:
                    if len(cards_by_suit[suit]) >= 5 and self.__check_straight(cards_by_suit[suit]):
                        check = True
            case Combination.ROYAL_FLUSH:
                cards_by_suit = self.__group_suits(cards)
                for suit in cards_by_suit:
                    if len(cards_by_suit[suit]) >= 5 and min(cards_by_suit[suit]) == 10 and max(cards_by_suit[suit]) == 14 and self.__check_straight(cards_by_suit[suit]):
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
                    lowest_stake = Stake([self.stake.ranks[0]+1], current_combo)
                    lowest_stake = lowest_stake if self.stake.ranks[0]+1 <= 14 else lowest_next_stake
                case Combination.TWO_PAIR:
                    biggest_value = max(self.stake.ranks)
                    lowest_value = min(self.stake.ranks)
                    lowest_stake = Stake([biggest_value, lowest_value+1], current_combo)
                    lowest_stake = lowest_stake if lowest_value+1 <= 14 else lowest_next_stake
                case Combination.STRAIGHT | Combination.STRAIGHT_FLUSH:
                    biggest_value = max(self.stake.ranks)
                    lowest_value = min(self.stake.ranks)
                    ranks = [i for i in range(lowest_value+1, biggest_value+2)]
                    lowest_stake = Stake(ranks, current_combo)
                    lowest_stake = lowest_stake if biggest_value+1 <= 14 else lowest_next_stake
                case Combination.FLUSH | Combination.ROYAL_FLUSH:
                    lowest_stake = lowest_next_stake
                case Combination.FULL_HOUSE:
                    tris = self.stake.ranks[0]
                    bis = self.stake.ranks[1]
                    if bis < tris:
                        bis = bis + 2
                        lowest_stake = Stake([tris, bis], current_combo)
                        lowest_stake = lowest_stake if bis <= 13 else lowest_next_stake
                    else:
                        tris = tris + 1
                        bis = bis - 1
                        lowest_stake = Stake([tris, bis], current_combo)
                        lowest_stake = lowest_stake if tris <= 14 else lowest_next_stake
        return lowest_stake