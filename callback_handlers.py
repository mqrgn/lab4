from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from api import get_crypto_info, get_watchlist_prices
from states import CryptoState
from user_watchlist import user_watchlists


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

    await callback.message.edit_text(
        "✍️ <b>Введите название криптовалюты</b>\n"
        "(например: <code>bitcoin</code>, <code>ethereum</code>, <code>toncoin</code>)",
        reply_markup=kb)

    await state.set_state(CryptoState.waiting_for_coin_name)


async def like_callback(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id

    user_coins = user_watchlists.get(user_id, [])

    if not user_coins:
        kb1 = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Добавить", callback_data="add")],
            [types.InlineKeyboardButton(text="Назад", callback_data="menu")]])
        text = get_watchlist_prices(user_coins)
        await callback.message.edit_text(text, reply_markup=kb1)

    else:
        kb2 = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Добавить", callback_data="add")],
            [types.InlineKeyboardButton(text="Удалить", callback_data="delete")],
            [types.InlineKeyboardButton(text="Назад", callback_data="menu")]])
        text = get_watchlist_prices(user_coins)
        await callback.message.edit_text(text, reply_markup=kb2)


async def add_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        "Введите ID монеты для добавления (например: <code>bitcoin</code>):")
    await state.set_state(CryptoState.waiting_for_watchlist_add)


async def delete_callback(callback: types.CallbackQuery, state: FSMContext) -> None:

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Отмена", callback_data="like")]
    ])

    await callback.message.edit_text(
        "<b>Введите название монеты для удаления:</b>\n"
        "(например: <code>bitcoin</code>, <code>solana</code>)",
        reply_markup=kb
    )

    await state.set_state(CryptoState.waiting_for_watchlist_delete)


async def menu_callback(callback: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Избранное", callback_data="like")],
                         [types.InlineKeyboardButton(text="BITCOIN", callback_data="btc")],
                         [types.InlineKeyboardButton(text="ETHEREUM", callback_data="eth")],
                         [types.InlineKeyboardButton(text="SOLANA", callback_data="sol")],
                         [types.InlineKeyboardButton(text="Ввести свою криптовалюту", callback_data="own")]])
    await callback.message.edit_text(f"Я могу показать курс криптовалюты, "
                                     f"\nкоторую ты мне введешь", reply_markup=kb)


def register_callback_handlers(dp: Dispatcher) -> None:
    dp.callback_query.register(btc_callback, F.data == "btc")
    dp.callback_query.register(eth_callback, F.data == "eth")
    dp.callback_query.register(sol_callback, F.data == "sol")
    dp.callback_query.register(menu_callback, F.data == "menu")
    dp.callback_query.register(own_callback, F.data == "own")
    dp.callback_query.register(like_callback, F.data == "like")
    dp.callback_query.register(add_callback, F.data == "add")
    dp.callback_query.register(delete_callback, F.data == "delete")
