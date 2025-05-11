from nicegui import ui
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import LowestStake, Stake
from src.model.stake.combination import Combination
from utils.state import user_state
from src.services.connection.topic import Topic
from src.services.connection.topic import game_topics
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler

# URL di default per il dorso delle carte (devi servirlo con ui.add_static_files o CDN)
BACK_IMAGE_URL = './static/back_small.png'

def opponent_card(
    name: str,
    avatar_color: str = 'blue',      # nome colore Tailwind (es. 'red','green','blue','indigo'...)
    card_images: list[str] = None,    # lista di URL, lunghezza 1–5
    current_player: bool = False
):
    card_images = card_images or [BACK_IMAGE_URL] * 5
    # Wrapper verticale centrato
    with ui.column().classes('items-center mx-4 gap-0') as container:
        if current_player:
            ui.element('div').classes('border-solid border-t-black border-t-8 border-x-transparent border-x-8 border-b-0 mb-2')
        else:
            ui.element('div').classes('border-solid border-t-transparent border-t-8 border-x-transparent border-x-8 border-b-0 mb-2 opacity-0')
        # Avatar circolare
        ui.element('div')\
          .classes(f'bg-{avatar_color}-500 rounded-full')\
          .style('width:55px; height:55px;')
        # Nome sotto l’avatar (opzionale)
        ui.label(name).classes('mt-2 font-semibold')
        # Fila di carte
        with ui.row().classes('mt-2 gap-0'):
            for img in card_images:
                ui.image(source=img)\
                  .classes('w-12 h-18 m-1')\
                  .on('click', lambda img=img: ui.notify(f'Hai cliccato su {img}'))
    return container

def stake_card(stake_string: str):
    with ui.element('div').classes('stake-card') as container:
        ui.label(f'\"{stake_string}\"').classes('text-6xl font-bold text-gray-800')
    return stake_string




def setup():
    from src.view.utils.layout import centered_layout
    from src.view.components.dialogs import cards_picker, combination_picker
    
    message_factory = MessageFactory()

    __player_colors = [
        'red', 'blue', 'green', 'yellow',
        'purple', 'orange', 'pink', 'brown',
        'cyan', 'lime'
    ]
    
    is_my_turn = False

    @ui.page('/game')
    def game_page():
        players: list[Player] = []
        player: Player = Player(
            user_state.username, user_state.id)
        min_stake: Stake = LowestStake.HIGH_CARD.value
        moves_label = None
        
        
        
        def on_start_game():
            nonlocal players
            #ui.notify('on_start_game')
            message = connection_handler.no_wait_message(
                "lobby/" + str(user_state.selected_lobby) + Topic.START_ROUND)
            if message:
                players_msg: list[Player] = message.body["players"]
                players = [p for p in players_msg if p.id != player.id]
                player.cards = [p for p in players_msg if p.id == player.id][0].cards
                ui.notify(f'Game started with players: {players}')
                ui.notify(f'Cards in hand: {player.cards_in_hand}')
                content.refresh()
                

        ui.timer(1, on_start_game)
        
        @ui.refreshable 
        def content():
            ui.add_head_html('''
              <!-- Definisci utility arbitrarie per grid-template-rows -->
              <style>
                .nicegui-content {
                  height: 100vh !important;
                  padding: 0 !important;
                }
                
                @layer utilities {
                  .grid-rows-[5%_25%_10%_5%_13%_37%_5%] {
                    grid-template-rows: 5% 25% 10% 5% 13% 37% 5%;
                  }
                }
                
                @font-face {
                font-family: 'CocoSharp Trial';
                src: url('/static/fonts/Coco-Sharp-Heavy-trial') format('truetype');
                font-weight: normal;
                font-style: normal;
                }
                .stake-card {
                  background-color: #e0e0e0;             /* grigio chiaro */
                  border-radius: 1rem;                   /* pill shape */
                  padding: 0.5rem 1.5rem;                /* verticale/orizzontale */
                  display: inline-block;
                  font-family: 'CocoSharp Trial', sans-serif;
                  font-size: 1.25rem;                    /* circa 20px */
                  font-weight: bold;
                  color: #333333;
                }
                button {
                    font-family: "CocoSharp Trial" !important;
                    border-radius: 1rem !important; 
                    color: white !important;
                    padding: 1rem !important; 
                    min-height: 0 !important;
                }
              </style>
            ''') 
            nonlocal is_my_turn
            # nonlocal min_stake
            async def show_stake_dialog(min_stake: Stake):
                # print("min stake dialog: " + min_stake)
                combo = await combination_picker(min_stake.combo)
                max_cards = 5
                match combo:
                    case (
                        Combination.HIGH_CARD
                        | Combination.PAIR
                        | Combination.THREE_OF_A_KIND
                        | Combination.FOUR_OF_A_KIND
                    ):
                        max_cards = 1
                    case (
                        Combination.TWO_PAIR
                        | Combination.FULL_HOUSE
                    ):
                        max_cards = 2
                cards = await cards_picker(max_cards=max_cards)
                if check_input(cards, combo):
                    ui.notify(f'You chose {combo} with cards {cards}')
                    ranks = [card.rank for card in cards]
                    suits = [card.suit for card in cards]
                    stake: Stake = Stake(combo, ranks, suits)
                    connection_handler.send_message(message_factory.create_raise_stake_message(player, stake), "lobby/" + str(user_state.selected_lobby) + Topic.RAISE_STAKE)
                else:
                    ui.notify('Invalid input!')

            def check_input(cards: list[Card], combo: Combination) -> bool:
                if combo == Combination.STRAIGHT:
                    cards.sort(key=lambda x: x.rank.value)
                    return all(
                        cards[i].rank.value == cards[i + 1].rank.value - 1
                        for i in range(len(cards) - 1)
                    )
                elif combo == Combination.FLUSH:
                    return all(
                        cards[i].suit == cards[i + 1].suit
                        for i in range(len(cards) - 1)
                    )
                elif combo == Combination.STRAIGHT_FLUSH:
                    cards.sort(key=lambda x: x.rank.value)
                    return all(
                        cards[i].suit == cards[i + 1].suit
                        for i in range(len(cards) - 1)
                    ) and all(
                        cards[i].rank.value == cards[i + 1].rank.value - 1
                        for i in range(len(cards) - 1)
                    )
                elif combo == Combination.ROYAL_FLUSH:
                    cards.sort(key=lambda x: x.rank.value)
                    return all(
                        cards[i].suit == cards[i + 1].suit
                        for i in range(len(cards) - 1)
                    ) and all(
                        cards[i].rank.value == Rank(i + 10).value
                        for i in range(len(cards))
                    )
                elif combo == Combination.HIGH_CARD or combo == Combination.PAIR or combo == Combination.THREE_OF_A_KIND or combo == Combination.FOUR_OF_A_KIND or combo == Combination.TWO_PAIR or combo == Combination.FULL_HOUSE:
                    return True
                    
            # with ui.row().classes('justify-center'):
            #     for i in range(len(players)):
            #         pl: Player = players[i]
            #         with ui.column().classes('col-2 items-center'):
            #             ui.icon(
            #                 'circle', color=__player_colors[i], size='1.5rem')
            #             ui.label(pl.username).classes('text-lg')
            #             with ui.row():
            #                 for _ in range(pl.cards_in_hand):
            #                     ui.image('static/back.png'
            #                              ).style('width: 0.7rem; height: auto')

            # ui.image('static/back.png'
            #          ).style('width: 6rem; height: auto'
            #                  ).classes('q-mr-xl')          
            
            # with ui.row():
            #     bullshit_btn = ui.button(
            #         'Bullsh*t',
            #         on_click=lambda: connection_handler.send_message(
            #             message_factory.create_check_liar_message(),
            #             "lobby/" + str(user_state.selected_lobby) + Topic.CHECK_LIAR
            #         ),
            #         color='red'
            #     ).style('width: 10rem; height: auto')
            #     bullshit_btn.set_enabled(is_my_turn)
            #     raise_btn = ui.button(
            #         'Raise',
            #         on_click=lambda: show_stake_dialog(min_stake),
            #         color='green'
            #     ).style('width: 10rem; height: auto')
            #     raise_btn.set_enabled(is_my_turn)
                
            def on_start_turn():
                nonlocal is_my_turn
                nonlocal min_stake
                message = connection_handler.no_wait_message(
                    "lobby/" + str(user_state.selected_lobby) + Topic.START_TURN)
                if message:
                    player: Player = message.body["player"]
                    min_stake = message.body["minimum_stake"]
                    if player.username == user_state.username:
                        ui.notify(f'Your turn!')
                        ui.notify(f'Minimum stake: {min_stake}')
                        is_my_turn = True
                    else:
                        ui.notify(f'{player.username}\'s turn!')
                        is_my_turn = False
                    content.refresh()
                    
            def on_player_move():
                nonlocal moves_label
                message = connection_handler.no_wait_message(
                    "lobby/" + str(user_state.selected_lobby) + Topic.RAISE_STAKE)
                if message:
                    pl: Player = message.body["player"]
                    stake: Stake = message.body["stake"]
                    moves_label.set_text(moves_label.text + '\n' +
                        f'{pl.username} raised {stake.combo} with cards {stake.ranks} of {stake.suits}')
                    
            def on_round_loser():
                message = connection_handler.no_wait_message(
                    "lobby/" + str(user_state.selected_lobby) + Topic.ROUND_LOSER)
                if message:
                    loser: Player = message.body["player"]
                    ui.notify(f'{loser.username} lost the round!')
                    cards_message = connection_handler.no_wait_message(
                        "lobby/" + str(user_state.selected_lobby) + Topic.SHOW_CARDS)
                    if cards_message:
                        cards: list[Card] = cards_message.body["cards"]
                        ui.notify(f'Cards in game: {cards}')
                        elimination_message = connection_handler.no_wait_message(
                            "lobby/" + str(user_state.selected_lobby) + Topic.ELIMINATION)
                        if elimination_message:
                            eliminated: Player = elimination_message.body["player"]
                            ui.notify(f'{eliminated.username} was eliminated!')
                            players.remove(eliminated)
                            if eliminated.username == user_state.username:
                                ui.notify('You were eliminated!')
                                ui.redirect('/lobby')
                    content.refresh()
                    
            ui.timer(1, on_start_turn)
            ui.timer(1, on_player_move)
            ui.timer(1, on_round_loser)
            
            # with ui.row():
            #     for card in player.cards:
            #         rank = card.rank
            #         suit = card.suit
            #         c: Card = Card(suit, rank)
            #         ui.image(f"static/{str(c.rank)}_of_{str(c.suit)}.png"
            #                  ).style('width: 6.5rem; height: auto'
            #                          ).classes('q-mx-sm')

            # with ui.row():
            #     ui.label(user_state.username).classes('text-lg')
            
            with ui.element('div').classes('bg-gray-100 flex items-center justify-center basis-full h-full w-full'):
                with ui.grid(rows='5% 25% 10% 5% 13% 37% 5%') \
                       .classes('w-full h-full max-w-full max-h-full grid-rows-[5%_25%_10%_5%_13%_37%_5%] border border-gray-300 gap-0 mx-[100px]'):
                    with ui.row().classes('flex items-center justify-center'):
                        # with ui.left_drawer().classes('bg-grey-2') as drawer:
                        #     ui.label('Moves:').classes('text-h6')
                        #     moves_label = ui.label('')
                        # drawer.value = False
                        # ui.button('☰ Moves', on_click=lambda: ui.left_drawer.toggle(drawer)).classes('m-4')
                        ...
                    with ui.row().classes('flex items-center justify-center'):
                        for i in range(len(players)):
                            pl: Player = players[i]
                            opponent_card(pl.username, avatar_color=__player_colors[i], card_images=[BACK_IMAGE_URL]*pl.cards_in_hand)
                    with ui.row().classes('flex items-center justify-center'):
                        stake_card('PAIR OF QUEENS')
                    with ui.row().classes('flex items-center justify-center'):
                        ...
                    with ui.row().classes('flex items-center justify-center'):
                        rise_button = ui.button('RISE STAKE')\
                            .classes('text-4xl font-bold')\
                            .style('background-color: #00999E !important;')\
                            .on('click', lambda: show_stake_dialog(min_stake))
                        rise_button.set_enabled(is_my_turn)
                        bullshit_button = ui.button('BULLSHIT')\
                            .classes('text-4xl font-bold')\
                            .style('background-color: #9E2500 !important;')\
                            .on('click', lambda: connection_handler.send_message(
                                message_factory.create_check_liar_message(),
                                "lobby/" + str(user_state.selected_lobby) + Topic.CHECK_LIAR
                            ))
                        bullshit_button.set_enabled(is_my_turn)
                    with ui.row().classes('flex items-center justify-center'):
                        for card in player.cards:
                            rank = card.rank
                            suit = card.suit
                            c: Card = Card(suit, rank)
                            ui.image(f"static/{str(c.rank)}_of_{str(c.suit)}.png")\
                                .style('width: 10%;')\
                                .classes('m-1')
                    with ui.row().classes('flex items-center justify-center'):
                        ...
                
        content()

