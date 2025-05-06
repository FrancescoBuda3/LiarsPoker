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

class Server(Debuggable):
    
    _LOBBY_SIZE = 10
    _MAX_LOBBIES = 1000
    _players: list[Player] = []
    _lobby: Dict[int, list[Player]] = {}
    _random = Random()
    _lobby_threads: Dict[int, list[Thread]] = {}
    _shutdown_event: threading.Event 

    def __init__(self, debug=True):
        Debuggable.__init__(self, debug)
        self._connection = ConnectionHandler(
            "Server", [t for t in Topic], debug=debug)
        self._message_factory = MessageFactory()
        self._shutdown_event = threading.Event()

    def run(self):
        topic, msg = self._connection.try_get_any_message()
        if msg is None:
            return
        #self._log(f"Received `{msg.body}` from `{topic}` topic")
        try:
            match topic:
                case Topic.NEW_LOBBY:
                    player = next((p for p in self._players if p.id == msg.body["player_id"]), None)
                    #if msg.body["lobby_id"] not in self._lobby.keys():
                    lobby_id = self.__create_lobby(player)
                    # self.client.subscribe(f"lobby/{id}")
                    self._log(f"New lobby created. ID: {lobby_id}")
                    self._connection.send_message(
                        self._message_factory.create_new_lobby_message(player.id, lobby_id), Topic.NEW_LOBBY)
                case Topic.NEW_PLAYER:
                    self.__new_player(msg.body["player"])
                case Topic.NEW_GAME:
                    lobby_id = msg.body["lobby_id"]
                    players_in_lobby: list[Player] = []
                    for player in self._lobby[lobby_id]:
                        players_in_lobby.append(player)
                    thread = Thread(target=game_loop, args=(
                        players_in_lobby, 
                        lobby_id
                    ))
                    self._lobby_threads[lobby_id] = thread
                    thread.start()
                    self._log(f"New game started for lobby {lobby_id} with {len(players_in_lobby)} players.")
                    
                case Topic.JOIN_LOBBY:
                    player = next((p for p in self._players if p.id == msg.body["player_id"]), None)
                    status = self.__join_lobby(player, msg.body["lobby_id"])
                    self._connection.send_message(
                        self._message_factory.create_join_lobby_message(player.id, msg.body["lobby_id"], status), Topic.JOIN_LOBBY
                    )
                    self._log(f"Player joined lobby: {status}")

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
        
    def shutdown(self):
        self._log("Initiating server shutdown...")
        self._shutdown_event.set() # Segnala a tutti i thread di terminare

        # Copia delle chiavi per evitare problemi di modifica del dizionario durante l'iterazione
        lobby_ids = list(self._lobby_threads.keys())
        for lobby_id in lobby_ids:
            thread = self._lobby_threads.get(lobby_id)
            if thread and thread.is_alive():
                self._log(f"Waiting for lobby {lobby_id} thread (ID: {thread.ident}) to join...")
                thread.join(timeout=5) # Aspetta che il thread termini, con un timeout
                if thread.is_alive():
                    self._log(f"Lobby {lobby_id} thread (ID: {thread.ident}) did not terminate in time.")
                else:
                    self._log(f"Lobby {lobby_id} thread (ID: {thread.ident}) joined.")
            # Rimuovi il thread dal dizionario dopo aver tentato il join
            if lobby_id in self._lobby_threads:
                del self._lobby_threads[lobby_id]


        self._log("All lobby threads processed.")
        # Aggiungi qui la chiusura di altre risorse, es. la connessione
        if hasattr(self._connection, 'stop'): # Se la tua ConnectionHandler ha un metodo stop/close
            self._connection.stop()
        self._log("Server shutdown complete.")



if __name__ == "__main__":
    server = Server(debug=True)
    try:
        while not server._shutdown_event.is_set(): # Continua finché non viene segnalato lo shutdown
            server.run()
            # Potresti voler aggiungere un breve sleep qui se server.run() è molto veloce e non bloccante
            # per evitare un busy-waiting, ma try_get_any_message probabilmente gestisce già una forma di attesa.
            # time.sleep(0.01) # Esempio
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received.")
    finally:
        server.shutdown()
        print("Server has been shut down.")
