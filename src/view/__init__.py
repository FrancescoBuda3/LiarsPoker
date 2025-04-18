import os
from nicegui import ui
from routes import home, lobby, login, lobby_select, game

# Leggo due env var: PORT e CLIENT_ID
PORT      = int(os.getenv('PORT',      8080))
CLIENT_ID = os.getenv('CLIENT_ID', 'PlayerX')

# Imposto un env var che il tuo modulo globale di ConnectionHandler
# userà al volo (se lo leggi da os.getenv è già perfetto),
# oppure ti basta passare CLIENT_ID al broker dentro il file dei globals.
os.environ['CLIENT_ID'] = CLIENT_ID

from routes import home, lobby, login, lobby_select, game

home.setup()
login.setup()
lobby.setup()
lobby_select.setup()
game.setup()

# Disabilita il reload automatico per evitare doppio spawn
ui.run(host='127.0.0.1', port=PORT, title=f'Liars Poker – {CLIENT_ID}', reload=False)
