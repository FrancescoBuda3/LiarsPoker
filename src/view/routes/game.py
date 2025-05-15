from nicegui import ui
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import LowestStake, Stake
from src.model.stake.combination import Combination
from src.view.components.dialogs import suit_picker
from src.view.components.game import opponent_component, stake_display
from src.view.logic.game import check_cards_combination
from utils.state import user_state
from src.services.connection.topic import Topic
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler


def setup():
    from src.view.components.dialogs import cards_picker, combination_picker, cards_display, white_cards_picker

    message_factory = MessageFactory()

    __player_colors = [
        'red', 'blue', 'green', 'yellow',
        'purple', 'orange', 'pink', 'brown',
        'cyan', 'lime'
    ]

    @ui.page('/game')
    def game_page():
        players: list[Player] = []
        local_player: Player = Player(user_state.username, user_state.id)
        min_stake: Stake = LowestStake.HIGH_CARD.value
        latest_move: Stake = None
        player_turn: Player = None

        def __to_game_topic(topic: Topic):
            return "lobby/" + str(user_state.selected_lobby) + topic

        @ui.refreshable
        def content():
            async def show_stake_dialog(min_stake: Stake):
                stake: Stake = None
                combo = await combination_picker(min_stake.combo)
                min_rank: Rank = Rank.ONE
                suits: set[Suit] = {Suit.HEARTS,
                                    Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES}
                if min_stake.ranks and combo == min_stake.combo:
                    min_rank = min_stake.ranks[0]
                if len(min_stake.suits) > 0 and combo == min_stake.combo:
                    suits = min_stake.suits
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
                match combo:
                    case (
                        Combination.FLUSH
                        | Combination.ROYAL_FLUSH
                    ):
                        suit = await suit_picker(suits)
                        stake = Stake(combo, [], suit)
                    case Combination.STRAIGHT_FLUSH:
                        cards = await cards_picker(max_cards=max_cards, suits=suits, min_rank=min_rank)
                        if check_cards_combination(cards, combo):
                            stake = Stake(combo, [card.rank for card in cards], [
                                          card.suit for card in cards])
                    case _:
                        cards = await white_cards_picker(max_cards=max_cards, min_rank=min_rank)
                        if check_cards_combination(cards, combo):
                            stake = Stake(combo, [card.rank for card in cards])
                if stake:
                    connection_handler.send_message(message_factory.create_raise_stake_message(
                        local_player, stake), __to_game_topic(Topic.RAISE_STAKE))
                else:
                    ui.notify('Choose valid cards!')

            def wait_start_turn():
                nonlocal player_turn
                nonlocal min_stake
                message = connection_handler.no_wait_message(
                    __to_game_topic(Topic.START_TURN))
                if message:
                    player_turn = message.body["player"]
                    min_stake = message.body["minimum_stake"]
                    if player_turn.username == user_state.username:
                        ui.notify(f'Your turn!')
                    content.refresh()

            def wait_player_move():
                nonlocal latest_move
                message = connection_handler.no_wait_message(
                    __to_game_topic(Topic.RAISE_STAKE))
                if message:
                    latest_move = message.body["stake"]
                    content.refresh()

            def wait_round_loser():
                message = connection_handler.no_wait_message(
                    __to_game_topic(Topic.ROUND_LOSER))
                if message:
                    loser: Player = message.body["player"]
                    ui.notify(f'{loser.username} lost the round!')
                    cards_in_game: list[Card] = message.body["cards"]
                    if len(cards_in_game) > 0:
                        cards_display(cards_in_game, lambda: content.refresh()).open()
                    eliminated: bool = message.body["elimination"]
                    if eliminated:
                        ui.notify(f'{loser.username} was eliminated!')
                        if loser.username == local_player.username:
                            ui.notify('You were eliminated!')
                            local_player.cards = []

            ui.timer(1, wait_start_turn)
            ui.timer(1, wait_player_move)
            ui.timer(1, wait_round_loser)

            def is_my_turn():
                return player_turn and player_turn.id == local_player.id

            with ui.element('div')\
                    .classes('bg-gray-100 flex items-center justify-center basis-full h-full w-full'):
                with ui.grid(rows='5% 25% 10% 5% 13% 37% 5%')\
                       .classes('w-full h-full max-w-full max-h-full grid-rows-game border border-gray-300 gap-0 mx-[100px]'):
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
                                __to_game_topic(Topic.CHECK_LIAR)
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

                    def leave_game():
                        connection_handler.send_message(
                            message_factory.create_remove_player_message(
                                local_player.id),
                            __to_game_topic(Topic.REMOVE_PLAYER)
                        )
                        connection_handler.send_message(
                            MessageFactory().create_leave_lobby_message(
                                user_state.selected_lobby),
                            Topic.LEAVE_LOBBY
                        )
                        user_state.selected_lobby = None
                        user_state.host = False
                        ui.navigate.to('/lobby_select')

                    with ui.row().classes('flex items-center justify-center'):
                        ui.button('Leave Game').on('click', leave_game)

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
                local_player_data_list = [
                    p for p in players_msg if p.id == local_player.id]
                if local_player_data_list:
                    local_player.cards = local_player_data_list[0].cards
                    content.refresh()

        ui.timer(1, wait_start_game)

        def wait_game_over():
            message = connection_handler.no_wait_message(
                __to_game_topic(Topic.GAME_OVER))
            if message:
                winner: Player = message.body["player"]
                with ui.dialog() as game_over_dialog, ui.card():
                    ui.label(f'Congratulations {winner} won the game!')
                game_over_dialog.open()
                ui.timer(5, lambda: ui.navigate.to('/lobby'), once=True)

        ui.timer(1, wait_game_over)
