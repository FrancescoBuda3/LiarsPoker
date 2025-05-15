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

    ui.add_head_html('''
              <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
            ''', shared=True)
    
    ui.add_css('''
        .nicegui-content {
          height: 100vh !important;
          padding: 0 !important;
        }

        .stake-card {
          background-color: #e0e0e0;             
          border-radius: 1rem;                   
          padding: 0.5rem 1.5rem;                
          display: inline-block;
          font-family: 'Montserrat', sans-serif;
          font-size: 1.25rem;                    
          font-weight: bold;
          color: #333333;
        }
        button {
            font-family: "Montserrat" !important;
            font-weight: 700 !important;
            border-radius: 1rem !important; 
            color: white !important;
            padding: 1rem !important; 
            min-height: 0 !important;
        }
    ''', shared=True)
    
    ui.run(host='127.0.0.1', port=PORT, title=f'Liars Poker', reload=False, favicon='static/favicon.png')
