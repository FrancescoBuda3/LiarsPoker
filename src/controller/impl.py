from paho.mqtt import client as mqtt

from src.controller import IServer


broker = 'broker.emqx.io'
broker_address = "127.0.0.1"
port = 1883
topic = "python/mqtt"
client_id = f'SERVER'



class ServerImpl(IServer):
    def __init__(self):
        client = self.connect_mqtt()
        self.client = client
        
    # Callback che gestisce la ricezione di un messaggio
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
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
        client = mqtt.Client()

        # Connessione al broker
        client.connect(broker_address, port, 60)
        # client.subscribe(topic_receive)
        client.on_message = self.on_message  # Set the on_message callback
        client.loop_start()
        return client
    
    def create_lobby(self, player, name) -> int:
        return self.client._protocol
    
    
    
server = ServerImpl()
print(server.create_lobby("player", "name"))
