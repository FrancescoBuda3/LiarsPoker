import sys
from nicegui import ui
from routes import home, lobby, login, lobby_select, game

if __name__ == "__main__":
    PORT = sys.argv[1]
    home.setup()
    login.setup()
    lobby.setup()
    lobby_select.setup()
    game.setup()

    # Disabilita il reload automatico per evitare doppio spawn
    ui.run(host='127.0.0.1', port=PORT, title=f'Liars Poker', reload=False)
