from src.services.message import Header
from src.controller.message_factory.impl import MessageFactory
from src.model.game.GImpl import GameImpl, GamePhase
from src.model.player import Player
from src.model.stake import Stake
from src.model.stake.combination import Combination
from src.services.connection.impl import ConnectionHandler
from src.services.message import Message


def game_loop(players: list[Player], id: str):
    lobby_topic = f"lobby/{id}"
    game = GameImpl()
    connection_handler = ConnectionHandler(id, [lobby_topic])
    message_factory = MessageFactory()
    for p in players:
        game.addPlayer(p)
    game.startGame()
    while game.getPhase() != GamePhase.GAME_OVER:
        if (game.getPhase() == GamePhase.PLAYING):
            game.startRound()
            connection_handler.send_message(message_factory.create_start_round_message(game.get_players()), lobby_topic)
            connection_handler.send_message(message_factory.create_start_turn_message(game.get_current_player(), None), lobby_topic)
            
        msg: Message = connection_handler.wait_message(lobby_topic)
        
        match msg.header :
            case Header.RAISE_STAKE:
                next_min_stake = game.raise_stake(msg.body)
                connection_handler.send_message(message_factory.create_start_turn_message(game.get_current_player(), next_min_stake), lobby_topic)
                
            case Header.CHECK_LIAR:
                loser_player: Player = game.check_liar()
                connection_handler.send_message(message_factory.create_round_loser_message(loser_player), lobby_topic)
                if not loser_player in game.get_players():
                    connection_handler.send_message(message_factory.create_elimination_message(loser_player), lobby_topic)
                
