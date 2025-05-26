from ..game import *
from src.model.deck.impl import Deck
from src.model.player import Player
from src.model.stake.impl import StakeHandlerImpl




class GameCore(Game):
    STARTING_PLAYER_INDEX = 0
    STARTING_CARDS = 1
    MINIMUM_PLAYERS = 2
    MAX_CARDS = 5

    def __init__(self):
        self.__players = []
        self.__deck = Deck()
        self.__current_player_index = self.STARTING_PLAYER_INDEX
        self.__stake_handler = StakeHandlerImpl()

    def start_game(self):
        if len(self.__players) < self.MINIMUM_PLAYERS:
            raise ValueError("Cannot start without enough players")

    def add_player(self, player:Player):
        player.cards_in_hand = self.STARTING_CARDS
        self.__players.append(player)

    def remove_player(self, player:Player): self.__players.remove(player)

    def start_round(self) -> None:
        self.__stake_handler.reset_stake()
        hands = self.__deck.shuffle([player.cards_in_hand for player in self.__players])
        for i, hand in enumerate(hands):
            self.__players[i].cards = hand

    def __next_player_index(self): return (self.__current_player_index + 1) % len(self.__players)

    def __previous_player_index(self): return (self.__current_player_index + len(self.__players) - 1) % len(self.__players)

    def get_current_player(self): return self.__players[self.__current_player_index]

    def get_players(self): return self.__players
    
    def raise_stake(self, stake) :
        self.__stake_handler.stake = stake
        self.__current_player_index = self.__next_player_index()
        return self.__stake_handler.get_lowest_next_stake()
    
    def get_latest_stake(self): return self.__stake_handler.stake

    def check_liar(self):
        hands = [player.cards for player in self.__players]
        cards = [card for hand in hands for card in hand]
        isLiar = not self.__stake_handler.check_cards(cards)
        loser_index = self.__previous_player_index() if isLiar else self.__current_player_index
        self.__current_player_index = loser_index
        self.__players[loser_index].cards_in_hand += 1
        return self.__players[loser_index]

        
    

        