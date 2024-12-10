import json
import logging
import os

from src.utils import (filter_by_date_transacts, filter_transacts_by_card_number, get_conversion, get_stocks_prices,
                       get_top_transacts, read_file_xlsx, read_greeting)

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)  # pragma: no cover

logger = logging.getLogger("views")
file_handler = logging.FileHandler(os.path.join(logs_dir, "views.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_home_page_json_response(date_str: str) -> str | list:
    """Функция страницы главная, которая генерирует ответ"""
    logger.info("Функция страницы главная начала свою работу")
    try:
        logger.info("Попытка открыть файл 'user_settings.json'")
        with open("../user_settings.json") as json_file:
            logger.info("Загрузка данных из файла 'user_settings.json'")
            data = json.load(json_file)
        user_currencies = data["user_currencies"]
        user_stocks = data["user_stocks"]
        logger.info("Чтение файла с транзакциями")
        df_transacts = read_file_xlsx("../data/operations.xlsx")

        gritting = read_greeting()
        cart_info = filter_transacts_by_card_number(df_transacts)
        sorted_df = filter_by_date_transacts(df_transacts, date_str)
        top_transacts = get_top_transacts(sorted_df)
        currency_func = get_conversion(user_currencies)
        stocks_func = get_stocks_prices(user_stocks)

        final_json_str = {
            "greeting": gritting,
            "cards": cart_info,
            "top_transactions": top_transacts,
            "currency_rates": currency_func,
            "stock_prices": stocks_func,
        }
        logger.info("Формирование json строки")
        json_data = json.dumps(final_json_str, indent=4, ensure_ascii=False)
        logger.info("Функция страницы главная успешно завершила свою работу")
        return json_data
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        return []


# Пример использования функции
if __name__ == "__main__":
    user_input = "31.12.2021 16:44:00"
    print(get_home_page_json_response(user_input))
