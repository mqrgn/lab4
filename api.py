import requests


def get_crypto_info(coin_id):
    """
    Получает сводку по монете для Telegram-бота.
    coin_id: ID монеты на CoinGecko (например, 'bitcoin', 'ethereum', 'toncoin')
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # Параметры запроса
    params = {
        'vs_currency': 'usd',
        'ids': coin_id.lower(),
        'order': 'market_cap_desc',
        'per_page': 1,
        'page': 1,
        'sparkline': 'false'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Проверка: если список пустой, значит монета не найдена
        if not data:
            return f"❌ Монета с ID '<b>{coin_id}</b>' не найдена. Попробуйте ввести полное название (например, bitcoin)."

        # Берем первый элемент списка (так как запрашивали одну монету)
        coin = data[0]

        # Извлекаем данные
        name = coin['name']
        symbol = coin['symbol'].upper()
        price = coin['current_price']
        high_24h = coin['high_24h']
        low_24h = coin['low_24h']
        change_24h = coin['price_change_percentage_24h']

        # Определяем эмодзи тренда
        trend = "📈" if change_24h is not None and change_24h >= 0 else "📉"

        # Если change_24h None (бывает у новых монет), ставим 0
        change_val = change_24h if change_24h else 0.0

        # Собираем сообщение с HTML разметкой
        message = (
            f"📊 <b>Отчет по {name} ({symbol})</b>\n\n"
            f"💰 <b>Цена (Индекс):</b> ${price:,.2f}\n"
            f"{trend} <b>Изменение 24ч:</b> {change_val:.2f}%\n"
            f"🔄 <b>24ч Мин:</b> ${low_24h:,.2f}\n"
            f"🔄 <b>24ч Макс:</b> ${high_24h:,.2f}\n\n"
            f"<i>Данные: средневзвешенный курс CoinGecko</i>"
        )

        return message

    except Exception as e:
        return f"⚠️ Произошла ошибка при запросе: {e}"



# print(get_crypto_info("bitcoin"))
# print(get_crypto_info("the-open-network"))
# print(get_crypto_info("solana"))