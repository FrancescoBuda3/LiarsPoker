from typing import Protocol


class SeriliazerInterface(Protocol):
    """
    Interface for serializing objects
    """
    
    _primitive_types: tuple = (int, float, str, bool, type(None))
    _container_types: tuple = (list, set)
    
    def serialize(self, object: object) -> str:
        """
        Serializes an object to a json string
        
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
            object (object): the object to serialize to a json string

        Returns:
            str: a string representation of the object in json format
        """
        ...