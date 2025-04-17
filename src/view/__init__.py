from nicegui import ui
from routes import home, lobby, login, lobby_select, game

# Route setup
home.setup()
login.setup()
lobby.setup()
lobby_select.setup()
game.setup()

ui.run(title='Liars Poker', favicon='🃟')
