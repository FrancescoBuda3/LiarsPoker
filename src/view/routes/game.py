import asyncio
from nicegui import app, ui
from src.model.card import Card
from src.model.card.rank import Rank
from src.model.card.suit import Suit
from src.model.player import Player
from src.model.stake import LowestStake, Stake
from src.model.stake.combination import Combination
from src.view.components.dialogs import suit_picker
from src.view.components.drawer import hint_drawer
from src.view.components.game import opponent_component, stake_display
from src.view.logic.game import check_cards_combination, cards_permitted
from utils.state import user_state
from src.services.connection.topic import Topic
from src.controller.message_factory.impl import MessageFactory
from utils.connection import connection_handler, unsubscribe_from_game_topics


def setup(debug: bool = False):
    from src.view.components.dialogs import cards_picker, combination_picker, cards_display, white_cards_picker
    if debug:
        connection_handler.set_debug(True)

    message_factory = MessageFactory()

    __player_colors = [
        'red', 'blue', 'green', 'yellow',
        'purple', 'orange', 'pink', 'brown',
        'cyan', 'lime'
    ]

    @ui.page('/game')
    async def game_page():
        players: list[Player] = []
        local_player: Player = Player(user_state.username, user_state.id)
        min_stake: Stake = LowestStake.HIGH_CARD.value
        latest_move: Stake | None = None
        player_turn: Player | None = None
        data_cached = False
        wait_game_info_timer = None
        wait_start_game_timer = None
        

        await ui.context.client.connected()
        if app.storage.tab.get('id') is None:
            print('no data saved')
            app.storage.tab['username'] = user_state.username
            app.storage.tab['selected_lobby'] = user_state.selected_lobby
            app.storage.tab['id'] = user_state.id
        else:
            print('data saved')
            data_cached = True
            user_state.username = app.storage.tab['username']
            user_state.selected_lobby = app.storage.tab['selected_lobby']
            user_state.id = app.storage.tab['id']
            local_player.username = user_state.username
            local_player.id = user_state.id

        def __to_game_topic(topic: Topic) -> str:
            return "lobby/" + str(user_state.selected_lobby) + topic
        
        drawer = hint_drawer()
        drawer.toggle()

        @ui.refreshable
        def content():
            async def show_stake_dialog(min_stake: Stake):
                stake: Stake | None = None
                combo = await combination_picker(min_stake.combo)
                if combo == None:
                    ui.notify('Choose valid combination!')
                    return
                min_rank: Rank = Rank.ONE
                suits: list[Suit] = [Suit.HEARTS,
                                     Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]
                if min_stake.ranks and combo == min_stake.combo:
                    min_rank = min_stake.single_rank
                if len(min_stake.suits) > 0 and combo == min_stake.combo:
                    suits = min_stake.suits
                max_cards = cards_permitted(combo)
                match combo:
                    case (
                        Combination.FLUSH
                        | Combination.ROYAL_FLUSH
                    ):
                        suit = await suit_picker(combo, suits)
                        stake = Stake(combo)
                        stake.suit = suit
                    case Combination.STRAIGHT_FLUSH:
                        cards = await cards_picker(combo, max_cards, suits, min_rank)
                        if check_cards_combination(cards, combo):
                            stake = Stake(combo, [card.rank for card in cards], [
                                          card.suit for card in cards])
                    case Combination.FULL_HOUSE:
                        min_pair = min_rank
                        min_triple = min_rank
                        if combo == min_stake.combo:
                            min_pair = min_stake.pair_rank
                            min_triple = min_stake.triple_rank
                        three_of_a_kind: list[Card] = await white_cards_picker(
                            Combination.THREE_OF_A_KIND, max_cards=1, min_rank=min_triple)
                        pair: list[Card] = await white_cards_picker(
                            Combination.PAIR, max_cards=1, min_rank=min_pair)
                        if three_of_a_kind and pair and check_cards_combination(pair + three_of_a_kind, combo):
                            stake = Stake(combo)
                            stake.triple_rank = three_of_a_kind[0].rank
                            stake.pair_rank = pair[0].rank
                    case _:
                        cards: list[Card] = await white_cards_picker(combo, max_cards=max_cards, min_rank=min_rank)
                        if check_cards_combination(cards, combo):
                            stake = Stake(combo, [card.rank for card in cards])
                if stake and (len(stake.ranks) > 0 or len(stake.suits) > 0):
                    connection_handler.send_message(message_factory.create_raise_stake_message(
                        local_player, stake), "lobby/" + str(user_state.selected_lobby) + Topic.RAISE_STAKE)
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
                    if player_turn and player_turn.username == user_state.username:
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
                        cards_display(
                            cards_in_game, lambda: content.refresh()).open()
                    eliminated: bool = message.body["elimination"]
                    if eliminated:
                        ui.notify(f'{loser.username} was eliminated!')
                        if loser.username == local_player.username:
                            ui.notify('You were eliminated!')
                            local_player.cards = []

            def wait_server_error():
                message = connection_handler.no_wait_message(
                    Topic.SERVER_ERROR)
                if message:
                    error: str = message.body["error"]
                    ui.notify(
                        "Server error, you will be redirected to lobby")
                    user_state.reset_ready()
                    ui.timer(5, lambda: ui.navigate.to('/lobby'), once=True)

            ui.timer(1, wait_start_turn)
            ui.timer(1, wait_player_move)
            ui.timer(1, wait_round_loser)
            ui.timer(1, wait_server_error)

            def __is_player_turn(player: Player) -> bool:
                return player_turn != None and player_turn.id == player.id

            def leave_game():
                connection_handler.send_message(
                    message_factory.create_remove_player_message(
                        local_player.id),
                    __to_game_topic(Topic.REMOVE_PLAYER)
                )
                connection_handler.send_message(
                    message_factory.create_leave_lobby_message(
                        user_state.id,
                        user_state.selected_lobby),
                    Topic.LEAVE_LOBBY
                )
                unsubscribe_from_game_topics(user_state.selected_lobby)
                user_state.reset_lobby()
                ui.navigate.to('/lobby_select')

            with ui.element('div')\
                    .classes('bg-gray-100 flex items-center justify-center basis-full h-full w-full'):
                with ui.grid(rows='7% 23% 10% 5% 13% 37% 5%')\
                       .classes('w-full h-full max-w-full max-h-full grid-rows-game border border-gray-300 gap-0 mx-[100px]'):
                    with ui.row().classes('flex items-end justify-end p-2'):
                        with ui.element('div').classes('top-4 right-4 z-50')\
                                .style('padding: 5px;'):
                            ui.button('Hint').on('click', lambda: drawer.toggle())\
                                .classes('bg-red-500 text-white px-4 py-2 rounded shadow-lg hover:bg-red-600 transition')
                        ui.element('div').classes('flex-grow')
                        with ui.element('div').classes('top-4 right-4 z-50')\
                                .style('padding: 5px;'):
                            ui.button('Logout')\
                                .on('click', leave_game)\
                                .classes('bg-red-500 text-white px-4 py-2 rounded shadow-lg hover:bg-red-600 transition')
                        
                        
                    with ui.row().classes('flex items-center justify-center'):
                        for i in range(len(players)):
                            pl: Player = players[i]
                            opponent_component(
                                pl.username,
                                __player_colors[i],
                                pl.cards_in_hand,
                                __is_player_turn(pl)
                            )
                    with ui.row().classes('flex items-center justify-center'):
                        stake_display(latest_move)
                    ui.row().classes('flex items-center justify-center')
                    with ui.row().classes('flex items-center justify-center'):
                        rise_button = ui.button('RISE STAKE')\
                            .classes('text-4xl font-bold p-4')\
                            .style('background-color: #00999E !important;')\
                            .on('click', lambda: show_stake_dialog(min_stake))
                        rise_button.set_enabled(__is_player_turn(local_player))
                        bullshit_button = ui.button('BULLSHIT')\
                            .classes('text-4xl font-bold p-4')\
                            .style('background-color: #9E2500 !important;')\
                            .on('click', lambda: connection_handler.send_message(
                                message_factory.create_check_liar_message(),
                                __to_game_topic(Topic.CHECK_LIAR)
                            ))
                        bullshit_button.set_enabled(
                            __is_player_turn(local_player))
                    with ui.row().classes('flex items-center justify-center'):
                        for card in local_player.cards:
                            rank = card.rank
                            suit = card.suit
                            c: Card = Card(suit, rank)
                            ui.image(f"static/{str(c.rank)}_of_{str(c.suit)}.png")\
                                .style('width: 10%;')\
                                .classes('m-1')
                    ui.row().classes('flex items-center justify-center')

        content()

        def wait_start_game():
            message = connection_handler.no_wait_message(
                __to_game_topic(Topic.START_ROUND))
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

        

        def wait_game_info():
            nonlocal player_turn
            nonlocal latest_move
            nonlocal min_stake
            nonlocal players
            nonlocal local_player
            nonlocal wait_game_info_timer

            message = connection_handler.no_wait_message(
                __to_game_topic(Topic.GAME_INFO))
            if message and message.body["interested_player"].id == user_state.id and message.body["turn_player"] is not None:
                wait_game_info_timer.deactivate()
                players_msg: list[Player] = message.body["players"]
                turn_player_msg: Player = message.body["turn_player"]
                latest_stake_msg: Stake = message.body["latest_stake"]
                min_next_stake_msg: Stake = message.body["min_next_stake"]
                for p in players_msg:
                    if p.id != local_player.id:
                        players.append(p)
                for p in players_msg:
                    if p.id == local_player.id:
                        local_player.cards = p.cards
                        local_player.cards_in_hand = p.cards_in_hand
                player_turn = turn_player_msg
                latest_move = latest_stake_msg
                min_stake = min_next_stake_msg
                content.refresh()
                
        wait_game_info_timer = ui.timer(1, wait_game_info)
        wait_start_game_timer = ui.timer(1, wait_start_game)
        

        if data_cached:
            connection_handler.send_message(
                message_factory.create_game_info_message(interested_player=local_player), __to_game_topic(Topic.GAME_INFO))
            wait_game_info_timer.activate()
        else:
            wait_start_game_timer.activate()

        def wait_game_over():
            message = connection_handler.no_wait_message(
                __to_game_topic(Topic.GAME_OVER))
            if message:
                winner: Player = message.body["player"]
                with ui.dialog() as game_over_dialog, ui.card():
                    ui.label(
                        f'Congratulations {winner.username} won the game!')
                game_over_dialog.open()
                user_state.reset_ready()
                # app.storage.clear()
                ui.timer(5, lambda: ui.navigate.to('/lobby'), once=True)

        ui.timer(1, wait_game_over)
