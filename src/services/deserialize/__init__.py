
from typing import Protocol


class DeserializerInterface(Protocol):
    """
    Interface for deserializing objects
    """
    
    def deserialize(self, str) -> object:
        """
        Deserializes a json string to an object
        
        Accepted types are:
        - Primitive types:
            - int
            - float
            - str
            - bool
            - None
            
        - Container types:
            - list
            - set
            
        - dict
            
        - Message
            - Header
        
        - Player
        
        - Card
            - Suit
            - Rank
        
        - Stake
            - Combination
        
        Args:
            str: a string representation of the object in json format

        Returns: 
            object (object): the object to serialize to a json string
        """
        ...