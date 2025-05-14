from src.controller.message_factory.impl import MessageFactory
from src.model.card import Card
from src.model.game.GImpl import GameImpl, GamePhase
from src.model.player import Player
from src.model.stake import LowestStake
from src.services.connection.impl import ConnectionHandler
from src.services.connection.topic import Topic
from src.services.connection.topic import game_topics


def game_loop(players: list[Player], id: str):
    game = GameImpl()
    lobby_topic = Topic.LOBBY + id
    connection_handler = ConnectionHandler(
        id, [lobby_topic + t for t in game_topics]
    )
    message_factory = MessageFactory()
    for p in players:
        game.add_player(p)
    game.start_game()
    while game.get_phase() != GamePhase.GAME_OVER:
        if (game.get_phase() == GamePhase.PLAYING):
            game.start_round()
            connection_handler.send_message(
                message_factory.create_start_round_message(game.get_players()),
                lobby_topic + Topic.START_ROUND)
            connection_handler.send_message(
                message_factory.create_start_turn_message(
                    game.get_current_player(), LowestStake.HIGH_CARD.value),
                lobby_topic + Topic.START_TURN)

        (topic, msg) = connection_handler.try_get_any_message()
        if msg:
            topic = Topic(topic.split("/")[-1])
            match topic:
                case Topic.RAISE_STAKE:
                    next_min_stake = game.raise_stake(msg.body['stake'])
                    connection_handler.send_message(
                        message_factory.create_start_turn_message(
                            game.get_current_player(), next_min_stake),
                        lobby_topic + Topic.START_TURN)

                case Topic.CHECK_LIAR:
                    loser_player: Player = game.check_liar()
                    cards_in_game: list[Card] = []
                    for p in game.get_players():
                        for c in p.cards:
                            cards_in_game.append(c)
                    elimination = not loser_player in game.get_players()
                    connection_handler.send_message(
                        message_factory.create_round_loser_message(
                            loser_player,
                            cards_in_game,
                            elimination
                        ),
                        lobby_topic + Topic.ROUND_LOSER)

                case Topic.REMOVE_PLAYER:
                    player_id = msg.body['player_id']
                    player = None
                    for p in game.get_players():
                        if p.id == player_id:
                            player = p
                    if player:
                        game.remove_player(player)
                        connection_handler.send_message(
                            message_factory.create_round_loser_message(player, [], True),
                            lobby_topic + Topic.ROUND_LOSER
                        )
                
    connection_handler.send_message(
        message_factory.create_game_over_message(game.get_players()[0]),
        lobby_topic + Topic.GAME_OVER)
