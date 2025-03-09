from enum import Enum
from src.model.game import Game
from src.model.game.impl import GameCore


class GamePhase(Enum):
    WAITING_FOR_PLAYERS = 1
    PLAYING = 2
    PLAYERS_TURN = 3
    GAME_OVER = 4


class GameImpl(Game):

    def __init__(self):
        self.phase = GamePhase.WAITING_FOR_PLAYERS
        self.core = GameCore()
    
    def add_player(self, player):
        if self.phase != GamePhase.WAITING_FOR_PLAYERS:
            raise ValueError("Cannot add player while game is running")
        self.core.add_player(player)
    
    def remove_player(self, player):
        if (self.phase != GamePhase.WAITING_FOR_PLAYERS and self.phase != GamePhase.PLAYERS_TURN) or self.core.get_current_player() != player:
            raise ValueError("Cannot remove player while it is not their turn")
        self.core.remove_player(player)
        if len(self.core.get_players()) == 1:
            self.phase = GamePhase.GAME_OVER
        else:
            self.phase = GamePhase.PLAYING

    def start_game(self):
        if self.phase != GamePhase.WAITING_FOR_PLAYERS:
            raise ValueError("Cannot start game while game is running")
        self.core.start_game()
        self.phase = GamePhase.PLAYING

    def start_round(self):
        if self.phase != GamePhase.PLAYING:
            raise ValueError("Cannot start round in this phase")
        self.core.start_round()
        self.phase = GamePhase.PLAYERS_TURN

    def raise_stake(self, stake):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot raise stake while it is not the player's turn")
        self.core.raise_stake(stake)
        
    def check_liar(self):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot check liar while it is not the player's turn")
        loser = self.core.check_liar()
        if not loser.cardsInHand > GameCore.MAX_CARDS:
            self.phase = GamePhase.PLAYING
        else:
            self.remove_player(loser)
        return loser
    
    def get_players(self):
        return self.core.get_players()
    
    def get_current_player(self):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot get current player while it is not the player's turn")
        return self.core.get_current_player()
    
    def get_latest_stake(self):
        if self.phase != GamePhase.PLAYERS_TURN:
            raise ValueError("Cannot get latest stake while it is not the player's turn")
        return self.core.get_latest_stake()

    def getPhase(self):
        return self.phase
    

    
