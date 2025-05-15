from typing import Protocol

from src.services.connection.topic import Topic
from src.services.message import Message


class ConnectionHandlerInterface(Protocol):
    """
    Class for handling the connection for sending and receiving messages.
    One or more topics can be subscribed to.
    """
    
    def subscribe(self, topic: Topic | str):
        """
        Subscribe to a topic to receive messages.

        Args:
            topic (Topic): topic to subscribe to
        """
        ...
        
    def unsubscribe(self, topic: Topic | str):
        """
        Unsubscribe from a topic to stop receiving messages.

        Args:
            topic (Topic): topic to unsubscribe from
        """
        ...

    def send_message(self, message: Message, topic: Topic | str):
        """
        Sends a message to all the listeners subcribed to the topic

        Args:
            message (Message): message to send
            topic (Topic): topic to send the message to
        """
        ...

    def wait_message(self, topic: Topic | str, timeout=None) -> Message:
        """
        Waits for a message to be received on the topic.

        Args:
            topic (Topic): topic to listen to
            timeout (int): maximum time to wait for a message, if none waits indefinitely
        Returns:
            Message: message received
        """
        ...
    
    def try_get_any_message(self) -> tuple[Topic, Message]:
        """
        Try to get a message if present on any topic
        
        Returns:
            tuple[Topic, Message]: the topic and message, None if message isn't present
        """
        ...
        
    def no_wait_message(self, topic: Topic | str) -> Message:
        """
        Get a message if present on the topic, None if not present
        
        Returns:
            Message: message received
        """
        ...
