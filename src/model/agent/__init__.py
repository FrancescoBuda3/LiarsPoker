from src.model.game.GImpl import GameImpl, GamePhase
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination


def game_loop():
    game = GameImpl()
    game.addPlayer(Player("Player 1"))
    game.addPlayer(Player("Player 2"))
    game.startGame()
    while game.getPhase() != GamePhase.GAME_OVER:
        if (game.getPhase() == GamePhase.PLAYING):
            game.startRound()
        for p in game.getPlayers():
            print("Player: " + p.username)
            print(f"Cards in hand: {p.cardsInHand}")
            print(f"Hand: {p.cards}")
            print()
        msg = input("Enter your move " + game.getCurrentPlayer().username + ": ")
        stake = Stake([int(msg)], Combination.HIGH_CARD)
        if int(msg) == 0:
            loser = game.checkLiar()
            print(f"Loser is: {loser}")
        else:
            game.raiseStake(stake)
    print("Winner is: " + game.getPlayers()[0].username)