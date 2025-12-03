from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from api import get_crypto_info
from states import CryptoState


async def btc_callback(callback: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data='menu')]
    ])
    await callback.message.edit_text(get_crypto_info("bitcoin"), reply_markup=kb)


async def eth_callback(callback: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data='menu')]
    ])
    await callback.message.edit_text(get_crypto_info("ethereum"), reply_markup=kb)


async def sol_callback(callback: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data='menu')]
    ])
    await callback.message.edit_text(get_crypto_info("solana"), reply_markup=kb)


async def own_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Отмена", callback_data='menu')]
    ])

    # Редактируем сообщение: просим ввести название
    await callback.message.edit_text(
        "✍️ <b>Введите название криптовалюты</b>\n"
        "(например: <code>bitcoin</code>, <code>ethereum</code>, <code>toncoin</code>)",
        reply_markup=kb)

    # ВАЖНО: Устанавливаем состояние ожидания
    await state.set_state(CryptoState.waiting_for_coin_name)


async def menu_callback(callback: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="BITCOIN", callback_data="btc")],
                         [types.InlineKeyboardButton(text="ETHEREUM", callback_data="eth")],
                         [types.InlineKeyboardButton(text="SOLANA", callback_data="sol")],
                         [types.InlineKeyboardButton(text="Ввести свою криптовалюту", callback_data="own")]
                         ])
    await callback.message.edit_text(f"Я могу показать курс криптовалюты, "
                                     f"\nкоторую ты мне введешь", reply_markup=kb)


def register_callback_handlers(dp: Dispatcher) -> None:
    dp.callback_query.register(btc_callback, F.data == "btc")
    dp.callback_query.register(eth_callback, F.data == "eth")
    dp.callback_query.register(sol_callback, F.data == "sol")
    dp.callback_query.register(menu_callback, F.data == "menu")
    dp.callback_query.register(own_callback, F.data == "own")