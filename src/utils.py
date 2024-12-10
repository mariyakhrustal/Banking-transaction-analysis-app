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
file_handler = logging.FileHandler(os.path.join(logs_dir, "utils.log"), mode="w", encoding="utf-8")
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


def read_file_xlsx(file_path: str) -> Any:
    """Функция читает данные из файла и возвращает DataFrame"""
    try:
        logger.info(f"Попытка открыть файл: {file_path}")
        excel_data = pd.read_excel(file_path)
        logger.info("Файл успешно открыт")
        return excel_data
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        return []


def filter_transacts_by_card_number(df_transacts: pd.DataFrame) -> list[Any]:
    """
    Функция, которая возвращает:
    последние 4 цифры карты;
    общую сумму расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    """
    try:
        logger.info("Функция фильтрации по номеру карты начала свою работу")
        carts_dict = df_transacts[df_transacts["Сумма платежа"] < 0].groupby("Номер карты")["Сумма платежа"].sum()
        cart_info = [
            {
                "last_digits": str(cart_num)[-4:],
                "total_spent": abs(total_spent),
                "cashback": round(abs(total_spent) / 100, 2),
            }
            for cart_num, total_spent in carts_dict.items()
        ]
        logger.info("Функция фильтрации по номеру карты успешно завершила свою работу")
        return cart_info
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []


def get_conversion(currencies: list) -> Any:
    """Функция конвертирует валюту и возвращает сумму транзакции в рублях."""
    try:
        logger.info("Функция конвертации валют начала свою работу")
        currency_rates = []
        for currency in currencies:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            headers = {"apikey": currency_api_key}
            params = {"from": currency, "to": "RUB", "amount": 1}
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                logger.info("get запрос на получение курса валют успешно отправлен")
                data = response.json()
                result = {"currency": currency, "rate": round(float(data["result"]), 2)}
                currency_rates.append(result)
            else:
                logger.error(f"Ошибка API при получении курса валют: {response.status_code}")
                print(f"Ошибка API: {response.status_code}")
                return []
        if currency_rates:
            logger.info("Конвертация валют прошла успешно")
            return currency_rates
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        logger.error(f"Ошибка при конвертации: {e}")
        return []


def get_stocks_prices(stocks: list) -> Any:
    """Функция, получающая цены на акции"""
    stock_prices = []
    try:
        logger.info("Функция для получения стоимости акций начала свою работу")
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={currency_api_key}"
            response = requests.get(url, timeout=10, allow_redirects=False)
            if response.status_code == 200:
                logger.info("get запрос на получение цен на акции успешно отправлен")
                data = response.json()
                result = {"stock": stock, "price": round(float(data["Global Quote"]["05. price"]), 2)}
                stock_prices.append(result)
            else:
                logger.error(f"Ошибка API при получении цен на акции: {response.status_code}")
                print(f"Ошибка API: {response.status_code}")
                return []
        if stock_prices:
            logger.info("Операция по получению цен на акции прошла успешно")
            return stock_prices
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []


def filter_by_date_transacts(transacts_df: pd.DataFrame, end_date: str) -> Any:
    """Функция фильтрует транзакции по дате, возвращает датафрейм, вводимый формат даты: '%d.%m.%Y %H:%M:%S'"""
    try:
        logger.info("Функция фильтрации транзакций по дате начала свою работу")
        target_date = datetime.strptime(end_date, "%d.%m.%Y %H:%M:%S")
        first_day_of_month = target_date.replace(day=1)
        transacts_df["Дата операции"] = pd.to_datetime(transacts_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        filtered_df = transacts_df[
            (transacts_df["Дата операции"] >= first_day_of_month) & (transacts_df["Дата операции"] <= target_date)
        ]
        logger.info("Функция фильтрации транзакций по дате успешно завершила свою работу")
        return filtered_df
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []


def get_top_transacts(filtered_df: pd.DataFrame) -> list[dict]:
    """Функция для получения топ транзакций по сумме платежа"""
    try:
        logger.info("Функция по получению топ транзакций начала свою работу")
        top_5_transactions = filtered_df.nlargest(5, "Сумма операции")
        top_list = [
            {
                "date": transaction["Дата операции"].strftime("%d.%m.%Y"),
                "amount": transaction["Сумма операции"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
            for _, transaction in top_5_transactions.iterrows()
        ]
        logger.info("Функция по получению топ транзакций успешно завершила свою работу")
        return top_list
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Ошибка: {e}")
        return []
