import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

currency_api_key = os.getenv("CURRENCY_API_KEY")
stocks_api_key = os.getenv("STOCKS_API_KEY")


def read_greeting() -> str:
    """Функция для генерации приветствия пользователя"""
    current_time = datetime.now()
    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_file_xlsx(file_path: str) -> pd.DataFrame:
    """Функция читает данные из файла и возвращает DataFrame"""
    excel_data = pd.read_excel(file_path)
    return excel_data


def filter_transacts_by_card_number(df_transacts: pd.DataFrame) -> list[dict]:
    """
    Функция, которая возвращает:
    последние 4 цифры карты;
    общую сумму расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    """
    carts_dict = (
        df_transacts.loc[(df_transacts["Сумма платежа"] < 0)]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    cart_info = []
    for cart_num, sum_of_spent in carts_dict.items():
        total_spent = abs(sum_of_spent)
        cart_info.append(
            {"last_digits": {cart_num[-4:]}, "total_spent": {total_spent}, "cashback": {round(total_spent / 100, 2)}}
        )
    return cart_info


def get_conversion(currencies: list) -> Any:
    """Функция конвертирует валюту и возвращает сумму транзакции в рублях."""
    try:
        currency_rates = []
        for currency in currencies:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            headers = {"apikey": currency_api_key}
            params = {"from": currency, "to": "RUB", "amount": 1}
            response = requests.get(url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result = {"currency": currency, "rate": round(float(data["result"]), 2)}
                currency_rates.append(result)
            else:
                print(f"Ошибка API: {response.status_code}")
                return []
        if currency_rates:
            return currency_rates
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return []


def get_stocks_prices(stocks: list) -> Any:
    """Функция, получающая цены на акции"""
    stock_prices = []
    try:
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={currency_api_key}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                data = response.json()
                result = {"stock": stock, "price": round(float(data["Global Quote"]["05. price"]), 2)}
                stock_prices.append(result)
            else:
                print(f"Ошибка API: {response.status_code}")
                return []
        if stock_prices:
            return stock_prices
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return []


# if __name__ == '__main__':
#     print(get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]))
# df = read_file_xlsx("../data/operations.xlsx")
# print(filter_transacts_by_card_number(df))
# print(get_conversion(["USD", "EUR"]))
