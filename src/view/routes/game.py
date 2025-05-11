from nicegui import ui
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.player import Player
from src.model.stake import LowestStake, Stake
from src.model.stake.combination import Combination
from utils.state import user_state
from src.services.connection.topic import Topic
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler

def opponent_component(
    name: str,
    avatar_color: str,
    cards: int,
    current_player: bool
):
    card_images = ['./static/back_small.png'] * cards
    current_player_class = 'border-t-black' if current_player else 'border-t-transparent opacity-0'
    with ui.column().classes('items-center mx-4 gap-0') as opponent_container:
        ui.element('div')\
            .classes(
                f'border-solid border-t-8 border-x-transparent border-x-8 border-b-0 mb-2 {current_player_class}')
        ui.element('div')\
          .classes(f'bg-{avatar_color}-500 rounded-full')\
          .style('width:55px; height:55px;')
        ui.label(name).classes('mt-2 font-semibold')
        with ui.row().classes('mt-2 gap-0'):
            for img in card_images:
                ui.image(source=img)\
                  .classes('w-12 h-18 m-1')
    return opponent_container

def stake_display(stake: Stake):
    with ui.element('div').classes('stake-card') as stake_container:
        if stake:
            ui.label(f'\"{stake.combo} of {stake.ranks[0].to_symbol()}\"')\
                .classes('text-6xl font-bold text-gray-800')
    return stake_container

def setup():
    from src.view.components.dialogs import cards_picker, combination_picker

    message_factory = MessageFactory()

    __player_colors = [
        'red', 'blue', 'green', 'yellow',
        'purple', 'orange', 'pink', 'brown',
        'cyan', 'lime'
    ]

    @ui.page('/game')
    def game_page():
        players: list[Player] = []
        local_player: Player = Player(
            user_state.username, user_state.id)
        min_stake: Stake = LowestStake.HIGH_CARD.value
        latest_move: Stake = None
        player_turn: Player = None
        
        ui.add_head_html('''
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
                src: url('/static/fonts/Coco-Sharp-Heavy-trial.ttf') format('truetype');
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

        @ui.refreshable
        def content():
            async def show_stake_dialog(min_stake: Stake):
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
                    ranks = [card.rank for card in cards]
                    suits = [card.suit for card in cards]
                    stake: Stake = Stake(combo, ranks, suits)
                    connection_handler.send_message(message_factory.create_raise_stake_message(
                        local_player, stake), "lobby/" + str(user_state.selected_lobby) + Topic.RAISE_STAKE)
                else:
                    ui.notify('Choose valid cards!')

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

            def wait_start_turn():
                nonlocal player_turn
                nonlocal min_stake
                message = connection_handler.no_wait_message(
                    "lobby/" + str(user_state.selected_lobby) + Topic.START_TURN)
                if message:
                    player_turn = message.body["player"]
                    min_stake = message.body["minimum_stake"]
                    if player_turn.username == user_state.username:
                        ui.notify(f'Your turn!')
                    else:
                        ui.notify(f'{player_turn.username}\'s turn!')
                    content.refresh()

            def wait_player_move():
                nonlocal latest_move
                message = connection_handler.no_wait_message(
                    "lobby/" + str(user_state.selected_lobby) + Topic.RAISE_STAKE)
                if message:
                    latest_move = message.body["stake"]
                    content.refresh()

            def wait_round_loser():
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

            ui.timer(1, wait_start_turn)
            ui.timer(1, wait_player_move)
            ui.timer(1, wait_round_loser)
            
            def is_my_turn():
                return player_turn and player_turn.id == local_player.id

            with ui.element('div')\
                .classes('bg-gray-100 flex items-center justify-center basis-full h-full w-full'):
                with ui.grid(rows='5% 25% 10% 5% 13% 37% 5%')\
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
                            opponent_component(
                                pl.username,
                                __player_colors[i], 
                                pl.cards_in_hand,
                                player_turn and player_turn.id == pl.id
                            )
                    with ui.row().classes('flex items-center justify-center'):
                        stake_display(latest_move)
                    with ui.row().classes('flex items-center justify-center'):
                        ...
                    with ui.row().classes('flex items-center justify-center'):
                        rise_button = ui.button('RISE STAKE')\
                            .classes('text-4xl font-bold')\
                            .style('background-color: #00999E !important;')\
                            .on('click', lambda: show_stake_dialog(min_stake))
                        rise_button.set_enabled(is_my_turn())
                        bullshit_button = ui.button('BULLSHIT')\
                            .classes('text-4xl font-bold')\
                            .style('background-color: #9E2500 !important;')\
                            .on('click', lambda: connection_handler.send_message(
                                message_factory.create_check_liar_message(),
                                "lobby/" +
                                str(user_state.selected_lobby) +
                                Topic.CHECK_LIAR
                            ))
                        bullshit_button.set_enabled(is_my_turn())
                    with ui.row().classes('flex items-center justify-center'):
                        for card in local_player.cards:
                            rank = card.rank
                            suit = card.suit
                            c: Card = Card(suit, rank)
                            ui.image(f"static/{str(c.rank)}_of_{str(c.suit)}.png")\
                                .style('width: 10%;')\
                                .classes('m-1')
                    with ui.row().classes('flex items-center justify-center'):
                        ...
                        
        content()

        def wait_start_game():
            message = connection_handler.no_wait_message(
                "lobby/" + str(user_state.selected_lobby) + Topic.START_ROUND)
            if message:
                players_msg: list[Player] = message.body["players"]
                players.clear()
                for p in players_msg:
                    if p.id != local_player.id:
                        players.append(p)
                local_player.cards = [
                    p for p in players_msg if p.id == local_player.id][0].cards
                content.refresh()

        ui.timer(1, wait_start_game)
