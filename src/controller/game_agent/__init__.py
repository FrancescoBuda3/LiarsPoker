from src.controller.message_factory.impl import MessageFactory
from src.model.game.GImpl import GameImpl, GamePhase
from src.model.player import Player
from src.services.connection.impl import ConnectionHandler
from src.services.connection.topic import Topic

__game_topics = [
    Topic.SHOW_CARDS,
    Topic.START_TURN,
    Topic.START_ROUND,
    Topic.ROUND_LOSER,
    Topic.ELIMINATION,
    Topic.RAISE_STAKE,
    Topic.CHECK_LIAR
]


def game_loop(players: list[Player], id: str):
    game = GameImpl()
    lobby_topic = Topic.LOBBY + id
    connection_handler = ConnectionHandler(
        id, __game_topics.map(lambda t: lobby_topic + t))
    message_factory = MessageFactory()
    for p in players:
        game.addPlayer(p)
    game.startGame()
    while game.getPhase() != GamePhase.GAME_OVER:
        if (game.getPhase() == GamePhase.PLAYING):
            game.startRound()
            connection_handler.send_message(
                message_factory.create_start_round_message(game.get_players()),
                lobby_topic + Topic.START_ROUND)
            connection_handler.send_message(
                message_factory.create_start_turn_message(
                    game.get_current_player(), None),
                lobby_topic + Topic.START_TURN)

        (topic, msg) = connection_handler.try_get_any_message()

        match topic:
            case Topic.RAISE_STAKE:
                next_min_stake = game.raise_stake(msg.body)
                connection_handler.send_message(
                    message_factory.create_start_turn_message(
                        game.get_current_player(), next_min_stake),
                    lobby_topic + Topic.START_TURN)
            case Topic.CHECK_LIAR:
                loser_player: Player = game.check_liar()
                connection_handler.send_message(
                    message_factory.create_round_loser_message(loser_player),
                    lobby_topic + Topic.ROUND_LOSER)
                cards_in_game = game.get_players().map(lambda p: p.cards)
                connection_handler.send_message(
                    message_factory.create_show_cards_message(cards_in_game),
                    lobby_topic + Topic.SHOW_CARDS)
                if not loser_player in game.get_players():
                    connection_handler.send_message(
                        message_factory.create_elimination_message(
                            loser_player),
                        lobby_topic + Topic.ELIMINATION)
    
    connection_handler.send_message(
        message_factory.create_game_over_message(game.get_winner()),
        lobby_topic + Topic.GAME_OVER)
