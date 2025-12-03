from aiogram import types, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from api import get_crypto_info
from states import CryptoState


async def start_command(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="BITCOIN", callback_data="btc")],
                         [types.InlineKeyboardButton(text="ETHEREUM", callback_data="eth")],
                         [types.InlineKeyboardButton(text="SOLANA", callback_data="sol")],
                         [types.InlineKeyboardButton(text="Ввести свою криптовалюту", callback_data="own")]
                         ])
    await message.answer(f"Привет! Я могу показать курс криптовалюты, \nкоторую ты мне введешь", reply_markup=kb)


async def random_message_handler(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="BITCOIN", callback_data="btc")],
                         [types.InlineKeyboardButton(text="ETHEREUM", callback_data="eth")],
                         [types.InlineKeyboardButton(text="SOLANA", callback_data="sol")],
                         [types.InlineKeyboardButton(text="Ввести свою криптовалюту", callback_data="own")]
                         ])
    await message.answer(f"Я тебя не понимаю!!!\n\nЯ могу показать курс криптовалюты, "
                         f"\nкоторую ты мне введешь", reply_markup=kb)


async def coin_input(message: types.Message, state: FSMContext) -> None:
    user_text = message.text.strip()

    temp_msg = await message.answer("⏳ Получаю данные...")

    result_text = get_crypto_info(user_text)

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="В меню", callback_data='menu')]
    ])

    await temp_msg.delete()
    await message.answer(result_text, reply_markup=kb)

    await state.clear()


def register_message_handlers(dp: Dispatcher) -> None:
    dp.message.register(start_command, CommandStart())
    dp.message.register(coin_input, CryptoState.waiting_for_coin_name)
    dp.message.register(random_message_handler)
