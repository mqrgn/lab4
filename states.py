from aiogram.fsm.state import State, StatesGroup


class CryptoState(StatesGroup):
    waiting_for_coin_name = State()
    waiting_for_watchlist_add = State()
    waiting_for_watchlist_delete = State()