from email.header import Header
from src.controller.message_factory.impl import MessageFactory
from src.model.game.GImpl import GameImpl, GamePhase
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.services.connectionHandler.impl import ConnectionHandlerImpl
from src.services.deserialize.impl import Deserializer


def game_loop(players: list[Player], id: str):
    game = GameImpl()
    connection_handler = ConnectionHandlerImpl(id)
    message_factory = MessageFactory()
    deserializer = Deserializer()
    for p in players:
        game.addPlayer(p)
    game.startGame()
    while game.getPhase() != GamePhase.GAME_OVER:
        if (game.getPhase() == GamePhase.PLAYING):
            game.startRound()
            connection_handler.send_message(message_factory.create_start_round_message(game.get_players()))
            connection_handler.send_message(message_factory.create_start_turn_message(game.get_current_player(), None))
            
        msg = connection_handler.wait_message()
        
        match msg.header :
            case Header.RaiseStake:
                game.raise_stake(msg.body)
                connection_handler.send_message(message_factory.create_raise_stake_message(msg.body))
                
            case Header.CheckLiar:
                loser_player = game.check_liar()
                connection_handler.send_message(message_factory.create_check_liar_message())
                
