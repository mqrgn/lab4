import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns


def main():
    print("--- ЗАДАНИЕ ПО АНАЛИЗУ ДАННЫХ ---")

    # ==========================================
    # 1. ВЫБОР И ЗАГРУЗКА ДАННЫХ
    # ==========================================
    print("\nЗагрузка данных (Bitcoin и Ethereum за 2025 год)...")

    try:
        btc_ticker = yf.Ticker("BTC-USD")
        eth_ticker = yf.Ticker("ETH-USD")

        # Получаем исторические данные
        btc_data = btc_ticker.history(start="2025-01-01", end="2025-12-01")
        eth_data = eth_ticker.history(start="2025-01-01", end="2025-12-01")

        if btc_data.empty or eth_data.empty:
            print("❌ Ошибка: Не удалось скачать данные.")
            return

    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")
        return

    # Собираем данные в одну таблицу
    # Используем выравнивание индексов автоматически
    df = pd.DataFrame()
    df['BTC'] = btc_data['Close']
    df['ETH'] = eth_data['Close']

    print("✅ Данные успешно загружены.")
    print(df.head())  # Вывод первых 5 строк для отчета

    # ==========================================
    # ПОДГОТОВКА ДАННЫХ
    # ==========================================
    print("\n[2] Подготовка данных...")

    # Удаляем временные зоны из дат, чтобы не было конфликтов (tz-localize)
    df.index = df.index.tz_localize(None)

    # Проверка на пустые значения
    missing_values = df.isnull().sum().sum()
    print(f"Количество пропущенных значений: {missing_values}")

    if missing_values > 0:
        df = df.dropna()
        print("Пропущенные значения удалены.")
    else:
        print("Данные чистые, пропусков нет.")

    # ==========================================
    # ВИЗУАЛИЗАЦИЯ
    # ==========================================
    print("\n Визуализация...")

    plt.figure(figsize=(12, 6))

    # Рисуем BTC (левая шкала)
    ax1 = plt.gca()
    line1 = ax1.plot(df.index, df['BTC'], color='orange', label='Bitcoin (BTC)')
    ax1.set_ylabel('Цена Bitcoin ($)', color='orange')
    ax1.tick_params(axis='y', labelcolor='orange')

    # Рисуем ETH (правая шкала)
    ax2 = ax1.twinx()
    line2 = ax2.plot(df.index, df['ETH'], color='blue', label='Ethereum (ETH)')
    ax2.set_ylabel('Цена Ethereum ($)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.title('Сравнение цен Bitcoin и Ethereum (2025 г.)')
    ax1.set_xlabel('Дата')
    ax1.grid(True, alpha=0.3)

    # Легенда
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.show()

    # ==========================================
    # ПРОВЕРКА ГИПОТЕЗЫ
    # ==========================================
    print("\nПроверка статистической гипотезы...")
    print("Гипотеза: Курсы BTC и ETH сильно коррелируют (r >= 0.7).")

    # Считаем корреляцию
    correlation = df['BTC'].corr(df['ETH'])

    print(f"\nРезультат: Коэффициент корреляции Пирсона = {correlation:.4f}")

    print("⏳ Открываю график корреляции (Scatter Plot)...")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df['BTC'], y=df['ETH'])
    plt.title(f'Корреляция: r = {correlation:.2f}')
    plt.xlabel('Цена Bitcoin')
    plt.ylabel('Цена Ethereum')
    plt.grid(True)
    plt.show()


    print("\nИТОГ")
    if correlation >= 0.7:
        print("✅ Гипотеза ПОДТВЕРЖДЕНА.")
    else:
        print("❌ Гипотеза ОТВЕРГНУТА.")


if __name__ == "__main__":
    main()