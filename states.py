from aiogram.fsm.state import State, StatesGroup


class CryptoState(StatesGroup):
    waiting_for_coin_name = State()