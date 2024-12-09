import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

currency_api_key = os.getenv("CURRENCY_API_KEY")
stocks_api_key = os.getenv("STOCKS_API_KEY")

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)  # pragma: no cover


logger = logging.getLogger("utils")
file_handler = logging.FileHandler(os.path.join(logs_dir, "utils.log"), mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_greeting() -> str:
    """Функция для генерации приветствия пользователя"""
    current_time = datetime.now()
    logger.info("Функция начала свою работу.")
    if 6 <= current_time.hour < 12:
        logger.info("Функция успешно завершила свою работу.")
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        logger.info("Функция успешно завершила свою работу.")
        return "Добрый день"
    elif 18 <= current_time.hour < 24:
        logger.info("Функция успешно завершила свою работу.")
        return "Добрый вечер"
    else:
        logger.info("Функция успешно завершила свою работу.")
        return "Доброй ночи"


def read_file_xlsx(file_path: str) -> pd.DataFrame | list:
    """Функция читает данные из файла и возвращает DataFrame"""
    try:
        logger.info(f"Попытка открыть файл: {file_path}")
        excel_data = pd.read_excel(file_path)
        logger.info("Файл успешно открыт")
        return excel_data
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        return []


def filter_transacts_by_card_number(df_transacts: pd.DataFrame) -> list[dict]:
    """
    Функция, которая возвращает:
    последние 4 цифры карты;
    общую сумму расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    """
    carts_dict = df_transacts[df_transacts["Сумма платежа"] < 0].groupby("Номер карты")["Сумма платежа"].sum()
    cart_info = [
        {
            "last_digits": str(cart_num)[-4:],
            "total_spent": abs(total_spent),
            "cashback": round(abs(total_spent) / 100, 2),
        }
        for cart_num, total_spent in carts_dict.items()
    ]
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
        logger.error(f"Ошибка при конвертации: {e}")
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
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []


# if __name__ == '__main__':
# df = read_file_xlsx("../data/operations.xlsx")
# print(filter_transacts_by_card_number(df))
# print(get_stocks_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]))
# print(get_conversion(["USD", "EUR"]))
