import queue
import uuid
from paho.mqtt import client as mqtt

from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties
from paho.mqtt.subscribeoptions import SubscribeOptions
from src.services.connection import ConnectionHandlerInterface
from src.services.connection.topic import Topic
from src.services.deserialize.impl import Deserializer
from src.services.message import Message
from src.services.serialize.impl import Serializer
from src.utils.debug import Debuggable


broker = 'broker.emqx.io'
broker_address = "127.0.0.1"
port = 1883


class ConnectionHandler(ConnectionHandlerInterface, Debuggable):
    def __init__(self, name: str, topics: list[str], debug: bool = True):
        Debuggable.__init__(self, debug)
        self._client_id = f'CONN_HANDLER_{name}_{uuid.uuid4()}'
        self._topic_queues = {topic: queue.Queue() for topic in topics}
        self._serializer = Serializer()
        self._deserializer = Deserializer()
        self._client = self.__connect_mqtt(self._client_id)
        self._topics = topics
        props = Properties(PacketTypes.SUBSCRIBE)
        props.SubscriptionIdentifier = 1
        for topic in self._topics:
            self._client.subscribe(topic, options=SubscribeOptions(noLocal=True), properties=props)

    def __connect_mqtt(self, client_id: str):
        client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)

        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        client.connect(broker_address, port, keepalive=120)

        client.loop_start()
        return client

    def __on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            self._log("Connected to MQTT Broker!")
        else:
            self._log("Failed to connect, return code %d\n", rc)

    def __on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        message = msg.payload.decode()
        self._log(f"Received `{message}` from `{msg.topic}` topic\n\n")
        deserialized_message = self._deserializer.deserialize(message)
        self._topic_queues[msg.topic].put(deserialized_message)

    def send_message(self, message: Message, topic: Topic | str):
        serialized_message = self._serializer.serialize(message)
        result = self._client.publish(topic, serialized_message)
        status = result[0]
        if status == 0:
            self._log(
                f"Message '{serialized_message}' sent to topic '{topic}'")
        else:
            self._log(f"Failed to send message to topic '{topic}'")

    def wait_message(self, topic: Topic | str, timeout=None) -> Message | None:
        if topic in self._topic_queues:
            try:
                return self._topic_queues[topic].get(timeout=timeout)
            except queue.Empty:
                return None
    
    def try_get_any_message(self) -> tuple[Topic | str, Message] | tuple[None, None]:
        for topic, q in self._topic_queues.items():
            try:
                message = q.get_nowait()
                return topic, message
            except queue.Empty:
                continue
        return None, None
    
    def no_wait_message(self, topic: Topic | str) -> Message | None:
        if topic in self._topic_queues:
            try:
                return self._topic_queues[topic].get_nowait()
            except queue.Empty:
                return None
        return None
    
    def subscribe(self, topic: Topic | str):
        if topic not in self._topics:
            self._client.subscribe(topic)
            self._topics.append(topic)
            self._topic_queues[topic] = queue.Queue()
            self._log(f"Subscribed to topic '{topic}'")
        else:
            self._log(f"Already subscribed to topic '{topic}'")
            
    def unsubscribe(self, topic: Topic | str):
        if topic in self._topics:
            self._client.unsubscribe(topic)
            self._topics.remove(topic)
            del self._topic_queues[topic]
            self._log(f"Unsubscribed from topic '{topic}'")
        else:
            self._log(f"Not subscribed to topic '{topic}'")
    