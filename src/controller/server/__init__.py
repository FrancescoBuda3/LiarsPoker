from random import Random
from threading import Thread
from typing import Dict

from src.controller.game_agent import game_loop
from src.controller.message_factory.impl import MessageFactory
from src.model.player import Player
from src.services.connection.impl import ConnectionHandler
from src.utils.debug import Debuggable
from src.services.connection.topic import Topic

class Server(Debuggable):
    
    _LOBBY_SIZE = 10
    _MAX_LOBBIES = 1000
    _players: list[Player] = []
    _lobby: Dict[int, list[Player]] = {}
    _random = Random()
    _lobby_threads: Dict[int, list[Thread]] = {}

    def __init__(self, debug=True):
        Debuggable.__init__(self, debug)
        self._connection = ConnectionHandler(
            "Server", [t for t in Topic], debug=debug)
        self._message_factory = MessageFactory()

    def run(self):
        topic, msg = self._connection.try_get_any_message()
        if msg is None:
            return
        self._log(f"Received `{msg.body}` from `{topic}` topic")
        try:
            match topic:
                case Topic.NEW_LOBBY:
                    player = next((p for p in self._players if p.id == msg.body["player_id"]), None)
                    lobby_id = self.__create_lobby(player)
                    # self.client.subscribe(f"lobby/{id}")
                    self._log(f"New lobby created. ID: {lobby_id}")
                    self._connection.send_message(
                        self._message_factory.create_new_lobby_message(player.id, lobby_id), Topic.NEW_LOBBY)
                case Topic.NEW_PLAYER:
                    self.__new_player(msg.body["player"])
                case Topic.NEW_GAME:
                    thread = Thread(target=game_loop, args=(
                        self._players, msg.body["lobby"]))
                    self._lobby_threads[msg.body["lobby"]] = thread
                    thread.start()
                    self._log("New game started")
                case Topic.JOIN_LOBBY:
                    if self.__join_lobby(msg.body["player"], msg.body["lobby"]):
                        self._log("Player joined lobby")
                    else:
                        self._log("Player couldn't join lobby")
                case Topic.LEAVE_LOBBY:
                    if self.__leave_lobby(msg.body["player"], msg.body["lobby"]):
                        self._log("Player left lobby")
                    else:
                        self._log("Player couldn't leave lobby")
                case Topic.DISCONNECT_PLAYER:
                    if self.__disconnect_player(msg.body["player"]):
                        self._log("Player disconnected")
                    else:
                        self._log("Player not found")
                case Topic.DELETE_LOBBY:
                    if self.__delete_lobby(msg.body["player"], msg.body["lobby"]):
                        thread.join()
                        self._log("Lobby deleted")
                    else:
                        self._log("Lobby not found")
                case _:
                    self._log("Unknown topic")
        except KeyError as e:
            self._log(f"Unexpected message: {e}")

    def __generate_id(self) -> int:
        id = self._random.randint(0, self._MAX_LOBBIES)
        if id not in self._lobby.keys():
            return id
        else:
            return self.__generate_id()

    def __create_lobby(self, player) -> int:
        id = self.__generate_id()
        self._lobby[id] = [player]
        return id

    def __join_lobby(self, player, lobby):
        if lobby in self._lobby.keys() and player not in self._lobby[lobby] and len(self._lobby[lobby]) < self._LOBBY_SIZE:
            self._lobby[lobby].append(player)
            return True
        else:
            return False

    def __leave_lobby(self, player, lobby):
        if lobby in self._lobby.keys() and player in self._lobby[lobby]:
            self._lobby[lobby].remove(player)
            return True
        else:
            return False

    def __new_player(self, player):
        self._players.append(player)

    def __disconnect_player(self, player):
        if player in self._players:
            self._players.remove(player)
            if player in [player for lobby in self._lobby.values() for player in lobby]:
                for lobby in self._lobby.values():
                    if player in lobby:
                        lobby.remove(player)
            return True
        else:
            return False

    def __delete_lobby(self, player, lobby):
        if lobby in self._lobby.keys() and player in self._lobby[lobby]:
            del self._lobby[lobby]
            return True
        else:
            return False


if __name__ == "__main__":
    server = Server()
    while True:
        server.run()
