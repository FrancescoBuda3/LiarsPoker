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
        
        def on_start_game():
            message = connection_handler.no_wait_message(
                "lobby/" + str(user_state.selected_lobby) + Topic.START_ROUND)
            if message:
                players_msg: list[Player] = message.body["players"]
                players.extend([p for p in players_msg if p.id != player.id])
                player.cards.extend(
                    [p for p in players_msg if p.id == player.id][0].cards)
                ui.notify(f'Game started with players: {players}')
                ui.notify(f'Cards in hand: {player.cards_in_hand}')
                centered_layout(content)
                return False

        ui.timer(0.5, on_start_game)
        
        @ui.refreshable 
        def content():
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
                    connection_handler.send_message(message_factory.create_raise_stake_message(stake), "lobby/" + str(user_state.selected_lobby) + Topic.RAISE_STAKE)
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

            players_moves = {}

            def show_player_move(player, text):
                players_moves[player].set_text(f'"{text}"')

            with ui.row().classes('justify-center'):
                for i in range(len(players)):
                    player: Player = players[i]
                    with ui.column().classes('col-2 items-center'):
                        ui.icon(
                            'circle', color=__player_colors[i], size='1.5rem')
                        ui.label(player.username).classes('text-lg')
                        with ui.row():
                            for _ in range(player.cards_in_hand):
                                ui.image('static/back.png'
                                         ).style('width: 0.7rem; height: auto')
                        move = ui.label(''
                                        ).classes('text-lg text-gray-600'
                                                  ).style('min-height: 1.5rem')
                        players_moves[player.username] = move

            ui.image('static/back.png'
                     ).style('width: 6rem; height: auto'
                             ).classes('q-mr-xl')
                           
            with ui.row():
                bullshit_btn = ui.button(
                    'Bullsh*t',
                    on_click=lambda: ui.notify("Bullsh*t!"),
                    color='red'
                ).style('width: 10rem; height: auto')
                bullshit_btn.set_enabled(is_my_turn)
                raise_btn = ui.button(
                    'Raise',
                    on_click=lambda: show_stake_dialog(min_stake),
                    color='green'
                ).style('width: 10rem; height: auto')
                raise_btn.set_enabled(is_my_turn)
                
            def on_player_move():
                nonlocal is_my_turn
                nonlocal min_stake
                start_message = connection_handler.no_wait_message(
                    "lobby/" + str(user_state.selected_lobby) + Topic.START_TURN)
                if start_message:
                    player: Player = start_message.body["player"]
                    min_stake = start_message.body["minimum_stake"]
                    if player.username == user_state.username:
                        ui.notify(f'Your turn!')
                        ui.notify(f'Minimum stake: {min_stake}')
                        is_my_turn = True
                    else:
                        ui.notify(f'{player.username}\'s turn!')
                        is_my_turn = False
                    content.refresh()
                    
            ui.timer(1, on_player_move)
            

            with ui.row():
                for card in player.cards:
                    ui.image(f"static/{card.rank}_of_{card.suit}.png"
                             ).style('width: 6.5rem; height: auto'
                                     ).classes('q-mx-sm')

            with ui.row():
                ui.label(user_state.username).classes('text-lg')

