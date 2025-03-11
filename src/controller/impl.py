from paho.mqtt import client as mqtt

from src.controller import IServer


broker = 'broker.emqx.io'
broker_address = "127.0.0.1"
port = 1883
topics = ["new_lobby", "new_player", "new_game", "join_lobby", "disconnect_player"]
client_id = f'SERVER'



class ServerImpl(IServer):
    def __init__(self):
        client = self.connect_mqtt()
        self.client = client
        
    # Callback che gestisce la ricezione di un messaggio
    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        match msg.topic:
            case "new_lobby":
                # TODO: Call method to create a new lobby
                print("New lobby created")
            case "new_player":
                # TODO: Call method to add a new player
                print("New player joined")
            case "new_game":
                # TODO: Call method to start a new game
                print("New game started")
            case "join_lobby":
                # Call method to join a lobby
                print("Player joined lobby")
            case "disconnect_player":
                # Call method to disconnect a player
                print("Player disconnected")
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
    
    def create_lobby(self, player, name) -> int:
        return self.client._protocol
    
    
    
server = ServerImpl()
while True:
    pass
