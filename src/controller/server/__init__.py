from random import Random
from paho.mqtt import client as mqtt

broker = 'broker.emqx.io'
broker_address = "127.0.0.1"
port = 1883
topics = ["new_lobby", "new_player", "new_game",
    "join_lobby", "disconnect_player", "leave_lobby", "delete_lobby"]
client_id = f'SERVER'


class Server():

    players = []
    lobby = {}
    random = Random(1234)

    def __init__(self):
        client = self.connect_mqtt()
        self.client = client

    # Callback che gestisce la ricezione di un messaggio
    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        print(message)
        match msg.topic:
            case "new_lobby":
                id = self.__create_lobby(msg.player, msg.name)
                self.client.subscribe(f"lobby/{id}")
                print(f"New lobby created. ID: {id}")
            case "new_player":
                if self.__new_player(msg.player):
                    print("New player added")
                else:
                    print("Player already exists")
            case "new_game":
                # TODO: Call method to start a new game
                print("New game started")
            case "join_lobby":
                if self.__join_lobby(msg.player, msg.lobby):
                    print("Player joined lobby")
                else:
                    print("Player couldn't join lobby")
            case "leave_lobby":
                if self.__leave_lobby(msg.player, msg.lobby):
                    print("Player left lobby")
                else:
                    print("Player couldn't leave lobby")
            case "disconnect_player":
                if self.__disconnect_player(msg.player):
                    print("Player disconnected")
                else:
                    print("Player not found")
            case "delete_lobby":
                if self.__delete_lobby(msg.player, msg.lobby):
                    print("Lobby deleted")
                else:
                    print("Lobby not found")
            case _:
                print("Unknown topic")
        
    def on_connect(self, client, userdata, flags, rc):
            # For paho-mqtt 2.0.0, you need to add the properties parameter.
            # def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

    def connect_mqtt(self):
        
        # Set Connecting Client ID
        # Creazione del client MQTT
        client = mqtt.Client(client_id)

        # Connessione al broker

        client.on_connect = self.on_connect
        client.on_message = self.on_message  # Set the on_message callback
        client.connect(broker_address, port, keepalive=120)
        for topic in topics:
            client.subscribe(topic)

        # client.subscribe(topic_receive)

        client.loop_start()
        return client
    
    def __generate_id(self) -> int:
        if self.random.randint(0, 1000) not in self.lobby.keys():
            return self.random.randint(0, 1000)
        else:
            return self.__generate_id()
    
    def __create_lobby(self, player, name) -> int:
        id = self.__generate_id()
        self.lobby[id] = {"name": name, "players": [player]}
        return id
    
    def __join_lobby(self, player, lobby):
        if lobby in self.lobby.keys() and player not in self.lobby[lobby]["players"] and len(self.lobby[lobby]["players"]) < 10:
            self.lobby[lobby]["players"].append(player)
            return True
        else:
            return False
        
    def __leave_lobby(self, player, lobby):
        if lobby in self.lobby.keys() and player in self.lobby[lobby]["players"]:
            self.lobby[lobby]["players"].remove(player)
            return True
        else:
            return False
        
    def __new_player(self, player):
        if player not in self.players:
            self.players.append(player)
            return True
        else:
            return False
        
    def __disconnect_player(self, player):
        if player in self.players:
            self.players.remove(player)
            if player in [player for lobby in self.lobby.values() for player in lobby["players"]]:
                for lobby in self.lobby.values():
                    if player in lobby["players"]:
                        lobby["players"].remove(player)
            return True
        else:
            return False
        
    def __delete_lobby(self, player, lobby):
        if lobby in self.lobby.keys() and player in self.lobby[lobby]["players"]:
            del self.lobby[lobby]
            return True
        else:
            return False
    
    
    
if __name__ == "__main__":
    server = Server()
    while True:
        pass