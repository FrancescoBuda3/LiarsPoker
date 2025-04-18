import os
from src.services.connection.impl import ConnectionHandler
from src.services.connection.topic import Topic

client_id = os.getenv('CLIENT_ID', 'FixedName')
connection_handler = ConnectionHandler(name=client_id, topics=[Topic.NEW_PLAYER, Topic.NEW_LOBBY, Topic.NEW_GAME])