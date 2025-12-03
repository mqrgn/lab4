from aiogram import types, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from api import get_crypto_info, valid_coin
from states import CryptoState
from user_watchlist import user_watchlists


async def start_command(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Избранное", callback_data="like")],
                         [types.InlineKeyboardButton(text="BITCOIN", callback_data="btc")],
                         [types.InlineKeyboardButton(text="ETHEREUM", callback_data="eth")],
                         [types.InlineKeyboardButton(text="SOLANA", callback_data="sol")],
                         [types.InlineKeyboardButton(text="Ввести свою криптовалюту", callback_data="own")]
                         ])
    await message.answer(f"Привет! Я могу показать курс криптовалюты, \nкоторую ты мне введешь", reply_markup=kb)


async def random_message_handler(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Избранное", callback_data="like")],
                         [types.InlineKeyboardButton(text="BITCOIN", callback_data="btc")],
                         [types.InlineKeyboardButton(text="ETHEREUM", callback_data="eth")],
                         [types.InlineKeyboardButton(text="SOLANA", callback_data="sol")],
                         [types.InlineKeyboardButton(text="Ввести свою криптовалюту", callback_data="own")]
                         ])
    await message.answer(f"Я тебя не понимаю!!!\n\nЯ могу показать курс криптовалюты, "
                         f"\nкоторую ты мне введешь", reply_markup=kb)


async def coin_input_handler(message: types.Message, state: FSMContext) -> None:
    user_text = message.text.strip()

    temp_msg = await message.answer("⏳ Получаю данные...")

    result_text = get_crypto_info(user_text)

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="В меню", callback_data='menu')]
    ])

    await temp_msg.delete()
    await message.answer(result_text, reply_markup=kb)

    await state.clear()


async def add_watchlist_handler(message: types.Message, state: FSMContext):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='В меню', callback_data="menu")]
    ])
    coin_name = message.text.lower().strip()
    user_id = message.from_user.id

    # Инициализируем список для юзера, если его нет
    if user_id not in user_watchlists:
        user_watchlists[user_id] = []

    valid = valid_coin(coin_name)
    if valid == True:
        if coin_name not in user_watchlists[user_id]:
            user_watchlists[user_id].append(coin_name)
            await message.answer(f"✅ Монета <b>{coin_name}</b> добавлена в избранное!", reply_markup=kb)
        else:
            await message.answer(f"ℹ️ Монета <b>{coin_name}</b> уже в списке.", reply_markup=kb)

        await state.clear()
    else:
        await message.answer(valid, reply_markup=kb)


async def delete_coin_handler(message: types.Message, state: FSMContext):
    coin_name = message.text.lower().strip()
    user_id = message.from_user.id

    user_coins = user_watchlists.get(user_id, [])

    kb_menu = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="В меню", callback_data="menu")]
    ])

    if coin_name in user_coins:
        user_coins.remove(coin_name)
        # Обновляем словарь (хотя список изменяемый, но для надежности)
        user_watchlists[user_id] = user_coins

        await message.answer(
            f"✅ Монета <b>{coin_name}</b> успешно удалена из избранного.",
            reply_markup=kb_menu
        )
        await state.clear()
    else:
        await message.answer(
            f"⚠️ Монеты <b>{coin_name}</b> нет в вашем списке.\n"
            "Проверьте правильность написания и попробуйте еще раз ввести монету",
            reply_markup=kb_menu
        )




def register_message_handlers(dp: Dispatcher) -> None:
    dp.message.register(start_command, CommandStart())
    dp.message.register(coin_input_handler, CryptoState.waiting_for_coin_name)
    dp.message.register(add_watchlist_handler, CryptoState.waiting_for_watchlist_add)
    dp.message.register(delete_coin_handler, CryptoState.waiting_for_watchlist_delete)
    dp.message.register(random_message_handler)
