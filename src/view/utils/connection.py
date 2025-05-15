from src.services.connection.impl import ConnectionHandler
from src.services.connection.topic import Topic

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
    ]
)