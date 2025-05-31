import unittest

from src.services.connection.impl import ConnectionHandler
from src.services.message import Message


class TestConnectionHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TEST_TOPIC = "test"
        cls.TEST_MESSAGE_A = "Hello from A"

    def setUp(self):
        self.handler_a = ConnectionHandler("test_handler_a", topics=[])
        self.handler_b = ConnectionHandler("test_handler_b", topics=[])
        
    def test_wait_message(self):
        self.handler_a.subscribe(self.TEST_TOPIC)
        self.handler_b.subscribe(self.TEST_TOPIC)
        self.handler_a.send_message(self.TEST_MESSAGE_A, self.TEST_TOPIC)
        received_message = self.handler_b.wait_message(self.TEST_TOPIC, timeout=5)
        self.assertEqual(received_message, self.TEST_MESSAGE_A)
    
    def test_unsubscribe(self):
        self.handler_a.subscribe(self.TEST_TOPIC)
        self.handler_b.subscribe(self.TEST_TOPIC)
        self.handler_a.send_message(self.TEST_MESSAGE_A, self.TEST_TOPIC)
        received_message = self.handler_b.wait_message(self.TEST_TOPIC, timeout=5)
        self.assertEqual(received_message, self.TEST_MESSAGE_A)

        self.handler_b.unsubscribe(self.TEST_TOPIC)
        self.handler_a.send_message("This should not be received", self.TEST_TOPIC)
        received_message = self.handler_b.wait_message(self.TEST_TOPIC, timeout=2)
        self.assertIsNone(received_message)
    
    def test_try_get_any_message(self):
        self.handler_a.subscribe(self.TEST_TOPIC)
        self.handler_b.subscribe(self.TEST_TOPIC)
        self.handler_a.send_message(self.TEST_MESSAGE_A, self.TEST_TOPIC)
        
        topic = None
        message = None
        while topic is None and message is None:
            topic, message = self.handler_b.try_get_any_message()
        
        self.assertEqual(topic, self.TEST_TOPIC)
        self.assertEqual(message, self.TEST_MESSAGE_A)
        
        
if __name__ == "__main__":
    unittest.main()