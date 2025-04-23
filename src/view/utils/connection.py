import os
from src.services.connection.impl import ConnectionHandler
from src.services.connection.topic import Topic

connection_handler = ConnectionHandler(name="client", topics=[Topic.NEW_PLAYER, Topic.NEW_LOBBY, Topic.NEW_GAME, Topic.JOIN_LOBBY])