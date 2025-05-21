from src.services.connection.impl import ConnectionHandler
from src.services.connection.topic import Topic, game_topics

connection_handler = ConnectionHandler(
    name="client", 
    topics=[
        Topic.NEW_LOBBY,
        Topic.NEW_PLAYER,
        Topic.READY_TO_PLAY,
        Topic.START_GAME,
        Topic.JOIN_LOBBY,
        Topic.LEAVE_LOBBY,
        Topic.REMOVE_PLAYER,
        Topic.SERVER_ERROR
    ]
)

def subscribe_to_game_topics(lobby_id: int):
            for topic in game_topics:
                connection_handler.subscribe(
                    "lobby/" + str(lobby_id) + topic)

def unsubscribe_from_game_topics(lobby_id: int):
    for topic in game_topics:
        connection_handler.unsubscribe(
            "lobby/" + str(lobby_id) + topic)