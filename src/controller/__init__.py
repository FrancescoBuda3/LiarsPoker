class IServer():
    
    def create_lobby(self, player, name) -> int:
        """
        Args:
            player (Player): player who wants to create the lobby
            name (str): name of the lobby

        Returns:
            int: id of the lobby created
        """
        pass
    
    def join_lobby(self, player, lobby) -> bool:
        """
        Args:
            player (Player): player who wants to join the lobby
            lobby (int): lobby id to join

        Returns:
            bool: True if player successfully joined the lobby, False otherwise
        """
        pass
    
    def leave_lobby(self, player, lobby) -> bool:
        """
        Args:
            player (Player): player who wants to leave the lobby
            lobby (int): lobby id to leave

        Returns:
            bool: True if player successfully left the lobby, False otherwise
        """
        pass
    
    def start_game(self, player, lobby) -> bool:
        """
        Args:
            player (Player): player who wants to start the game
            lobby (int): lobby id to start the game

        Returns:
            bool: True if game successfully started, False otherwise
        """
        pass
    
    def delete_lobby(self, player, lobby) -> bool:
        """
        Args:
            player (Player): player who wants to delete the lobby
            lobby (int): lobby id to delete

        Returns:
            bool: True if lobby successfully deleted, False otherwise
        """
        pass
    
    def new_player(self, player) -> bool:
        """
        Args:
            player (Player): player to add

        Returns:
            bool: True if player successfully added, False otherwise
        """
        pass
    
    def disconnect_player(self, player) -> bool:
        """
        Args:
            player (Player): player to disconnect

        Returns:
            bool: True if player successfully disconnected, False otherwise
        """
        pass