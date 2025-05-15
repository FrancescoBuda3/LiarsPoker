from random import Random
from threading import Thread
import threading
from typing import Dict

from src.controller.game_agent import game_loop
from src.controller.message_factory.impl import MessageFactory
from src.model.player import Player
from src.services.connection.impl import ConnectionHandler
from src.utils.debug import Debuggable
from src.services.connection.topic import Topic

__LOBBY_SIZE = 10
__MAX_LOBBIES = 1000
__MAX_PLAYERS = __MAX_LOBBIES * __LOBBY_SIZE

class __Lobby:
    _id: int
    _players: list[(Player, bool)]
    agent: Thread
    
    def __init__(self, id: int):
        self._id = id
        self._players = []
        self.agent = None
        
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def players(self) -> list[Player]:
        return self._players
        
    def add_player(self, player: Player) -> bool:
        if len(self._players) < __LOBBY_SIZE and player not in [p[0] for p in self._players]:
            self._players.append((player, False))
            return True
        else:
            return False
        
    def remove_player(self, player: Player) -> bool:
        for p in self._players:
            if p[0] == player:
                self._players.remove(p)
                return True
        return False
    
    def set_player_status(self, player: Player, is_ready: bool) -> None:
        for p in self._players:
            if p[0] == player:
                p[1] = is_ready
                
    def is_ready(self) -> bool:
        for p in self._players:
            if not p[1]:
                return False
        return True
    
    def start_game(self) -> bool:
        if self.is_ready():
            self.agent = Thread(target=game_loop, args=(self._players, self._id))
            self.agent.start()
            return True
        else:
            return False
        
    def stop_game(self) -> bool:
        if self.agent and self.agent.is_alive():
            self.agent.join(timeout=5)
            
    def __str__(self):
        return f"Lobby({self._id})"
    
class __Lobbies_Handler:
    _lobbies: list[__Lobby]
    __random: Random
    
    def __init__(self):
        self._lobbies = []
        self.__random = Random()
        
    def __generate_id(self) -> int:
        id = self.__random.randint(0, __MAX_LOBBIES)
        if id not in self._lobbies.ids():
            return id
        else:
            return self.__generate_id()
        
    def create_lobby(self) -> int:
        if len(self._lobbies) >= __MAX_LOBBIES:
            return None
        id = self.__generate_id()
        new_lobby = __Lobby(id)
        self._lobbies.append(new_lobby)
        return id
        
    def get_lobby(self, id: int) -> __Lobby:
        for lobby in self._lobbies:
            if lobby.id == id:
                return lobby
        return None
    
    def get_lobby_players(self, id: int) -> list[Player]:
        for lobby in self._lobbies:
            if lobby.id == id:
                return lobby.players
        return None
        
    def remove_lobby(self, id: int) -> bool:
        for lobby in self._lobbies:
            if lobby.id == id:
                self._lobbies.remove(lobby)
                return True
        return False
    
    def ids(self) -> list[int]:
        ids = []
        for lobby in self._lobbies:
            ids.append(lobby.id)
        return ids
    
class Server(Debuggable):
    
    _players: list[Player] = []
    _lobbies: __Lobbies_Handler
    _shutdown_event: threading.Event 

    def __init__(self, debug=True):
        Debuggable.__init__(self, debug)
        self._lobbies = __Lobbies_Handler()
        self._connection = ConnectionHandler(
            "Server", [t for t in Topic], debug=debug)
        self._message_factory = MessageFactory()
        self._shutdown_event = threading.Event()

    def run(self):
        topic, msg = self._connection.try_get_any_message()
        if msg:
            try:
                match topic:
                    case Topic.NEW_LOBBY:
                        player = self.__get_player_by_id(msg.body["player_id"])
                        lobby_id = self._lobbies.create_lobby()
                        response: bool = True
                        if lobby_id:
                            self._lobbies.get_lobby(lobby_id).add_player(player)
                            self._log(f"New lobby created. ID: {lobby_id}")
                        else:
                            response = False
                            self._log("Lobby limit reached. Cannot create new lobby.")
                        self._connection.send_message(
                            self._message_factory.create_response_message(
                                player.id, response), 
                            Topic.NEW_LOBBY)
                    
                    case Topic.NEW_PLAYER:
                        player: Player = msg.body["player"]
                        response: bool = True
                        if len(self._players) < __MAX_PLAYERS:
                            self._players.append(player)
                            self._log(f"New {player} created.")
                        else:
                            response = False
                            self._log("Player limit reached. Cannot create new player.")
                        self._connection.send_message(
                            self._message_factory.create_response_message(
                                player.id, response), 
                            Topic.NEW_PLAYER)
                        
                    case Topic.READY_TO_PLAY:
                        player = self.__get_player_by_id(msg.body["player_id"])
                        lobby = self._lobbies.get_lobby(msg.body["lobby_id"])
                        player_ready = msg.body["ready"]
                        if lobby:
                            lobby.set_player_status(player, player_ready)
                            if lobby.is_ready():
                                lobby.start_game()
                                self._connection.send_message(
                                    self._message_factory.create_start_game_message(lobby.id), 
                                    Topic.START_GAME)
                                self._log(f"New game started for {lobby} with {len(lobby.players)} players.")
                            else:
                                self._log(f"{player} is {"not" if player_ready == False else ""} ready to play in lobby {lobby}.")
                        
                    case Topic.JOIN_LOBBY:
                        player = self.__get_player_by_id(msg.body["player_id"])
                        lobby = self._lobbies.get_lobby(msg.body["lobby_id"])
                        response: bool = True
                        if lobby and lobby.add_player(player):
                            self._log(f"{player} joined lobby {lobby}.")
                        else:
                            response = False
                            self._log(f"{player} couldn't join lobby {lobby}.")
                        self._connection.send_message(
                            self._message_factory.create_response_message(
                                player.id, response),
                            Topic.JOIN_LOBBY)
                        
                    case Topic.LEAVE_LOBBY:
                        lobby = self._lobbies.get_lobby(msg.body["lobby_id"])
                        player = self.__get_player_by_id(msg.body["player_id"])
                        if lobby and lobby.remove_player(player):
                            self._log(f"{player} left lobby")
                            if len(lobby.players) <= 0:
                                self._lobbies.remove_lobby(lobby.id)
                                self._log(f"{lobby} deleted")
                            else:
                                self._log(f"{lobby} not deleted")
                        else:
                            self._log(f"{player} couldn't leave lobby")
                    
                    case Topic.REMOVE_PLAYER:
                        player = self.__get_player_by_id(msg.body["player_id"])
                        if self.__remove_player(player):
                            self._log(f"{player} deleted")
                        else:
                            self._log(f"{player} not found")
                            
                    case _:
                        self._log("Unknown topic")
                        
            except KeyError as e:
                self._log(f"Unexpected message: {e}")

    def __get_player_by_id(self, player_id) -> Player:
        for player in self._players:
            if player.id == player_id:
                return player
        return None

    def __remove_player(self, player):
        if player in self._players:
            self._players.remove(player)
            return True
        else:
            return False
        
    def shutdown(self):
        self._log("Initiating server shutdown...")
        self._shutdown_event.set()

        for id in self._lobbies.ids():
            lobby = self._lobbies.get_lobby(id)
            thread = lobby.agent
            if thread and thread.is_alive():
                self._log(f"Waiting for {lobby} thread (ID: {thread.ident}) to join...")
                thread.join(timeout=5) 
                if thread.is_alive():
                    self._log(f"{lobby} thread (ID: {thread.ident}) did not terminate in time.")
                else:
                    self._log(f"{lobby} thread (ID: {thread.ident}) joined.")

        self._log("All lobby threads processed.")
        self._log("Server shutdown complete.")



if __name__ == "__main__":
    server = Server(debug=True)
    try:
        while not server._shutdown_event.is_set():
            server.run()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.shutdown()
        print("Server has been shut down.")
