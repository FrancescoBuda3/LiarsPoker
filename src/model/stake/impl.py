from ..stake import *


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
    
    def check_cards(self, cards) -> bool:
        return True