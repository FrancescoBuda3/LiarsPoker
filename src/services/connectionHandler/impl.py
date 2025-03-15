import queue
from src.services.connectionHandler import ConnectionHandler
from paho.mqtt import client as mqtt


broker = 'broker.emqx.io'
broker_address = "127.0.0.1"
port = 1883
client_id = f'CONN_HANDLER' 


class ConnectionHandlerImpl(ConnectionHandler):
    def __init__ (self, lobby_id):
        self.message_queue = queue.Queue()
        client = self.connect_mqtt()
        self.client = client
        self.lobby_id = lobby_id
        topic = f"lobby/{self.lobby_id}"
        self.client.subscribe(topic)
    

    def connect_mqtt(self):
        # Set Connecting Client ID
        # Creazione del client MQTT
        client = mqtt.Client(client_id)

        # Connessione al broker

        client.on_connect = self.__on_connect
        client.on_message = self.__on_message  # Set the on_message callback
        client.connect(broker_address, port, keepalive=120)

        client.loop_start()
        return client
    
    def send_message(self, message):
        topic = f"lobby/{self.lobby_id}"
        result = self.client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"Message '{message}' sent to topic '{topic}'")
        else:
            print(f"Failed to send message to topic '{topic}'")
    
    def wait_message(self, timeout=None):
        try:
            msg = self.message_queue.get(timeout=timeout)
            return msg
        except queue.Empty:
            return None
    
    def __on_connect(self, client, userdata, flags, rc):
            # For paho-mqtt 2.0.0, you need to add the properties parameter.
            # def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

    def __on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        self.message_queue.put((msg.topic, message))
        print(message)
        
            
                  