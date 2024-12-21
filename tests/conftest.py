from unittest import mock

import pandas as pd
import pytest


@pytest.fixture
def sample_data() -> dict:
    data = {
        "Дата операции": [
            "01.03.2019 12:00:00",
            "20.05.2019 03:00:00",
            "15.04.2019 15:30:00",
            "31.08.2019 20:00:00",
        ],
        "Сумма": [100, 200, 300, 400],
    }
    return data


@pytest.fixture
def sample_transact() -> pd.DataFrame:
    data = {
        "Дата операции": pd.to_datetime(
            ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06"]
        ),
        "Сумма операции": [1000, 2000, 1500, 3000, 2500, 500],
        "Категория": ["Продукты", "Транспорт", "Развлечения", "Путешествия", "Кафе", "Магазин"],
        "Описание": ["Покупка в магазине", "Билет на автобус", "Кино", "Отпуск", "Обед", "Кофе"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_dependencies():
    with mock.patch("src.views.read_file_xlsx") as mock_read_file_xlsx, mock.patch(
        "src.views.read_greeting"
    ) as mock_read_greeting, mock.patch(
        "src.views.filter_transacts_by_card_number"
    ) as mock_filter_transacts_by_card_number, mock.patch(
        "src.views.filter_by_date_transacts"
    ) as mock_filter_by_date_transacts, mock.patch(
        "src.views.get_top_transacts"
    ) as mock_get_top_transacts, mock.patch(
        "src.views.get_conversion"
    ) as mock_get_conversion, mock.patch(
        "src.views.get_stocks_prices"
    ) as mock_get_stocks_prices, mock.patch(
        "src.views.create_json_response"
    ) as mock_create_json_response:

        # Настроим моки с тестовыми значениями
        mock_read_file_xlsx.return_value = []  # Мокируем пустой DataFrame для чтения из Excel
        mock_read_greeting.return_value = "Hello, User!"  # Мокируем приветствие
        mock_filter_transacts_by_card_number.return_value = []  # Мокируем информацию о картах
        mock_filter_by_date_transacts.return_value = []  # Мокируем отсортированные транзакции
        mock_get_top_transacts.return_value = []  # Мокируем топ транзакций
        mock_get_conversion.return_value = {"USD": 1.0}  # Мокируем курсы валют
        mock_get_stocks_prices.return_value = {"AAPL": 150.0}  # Мокируем курсы акций
        mock_create_json_response.return_value = '{"greeting": "Hello, User!", "currency_rates": {"USD": 1.0}}'

        yield {
            "mock_read_file_xlsx": mock_read_file_xlsx,
            "mock_read_greeting": mock_read_greeting,
            "mock_filter_transacts_by_card_number": mock_filter_transacts_by_card_number,
            "mock_filter_by_date_transacts": mock_filter_by_date_transacts,
            "mock_get_top_transacts": mock_get_top_transacts,
            "mock_get_conversion": mock_get_conversion,
            "mock_get_stocks_prices": mock_get_stocks_prices,
            "mock_create_json_response": mock_create_json_response,
        }


@pytest.fixture
def example_data():
    data = [
        {"Категория": "Еда", "Дата операции": "15.09.2024 14:30:00", "Сумма платежа": -200},
        {"Категория": "Еда", "Дата операции": "10.10.2024 12:45:00", "Сумма платежа": -150},
        {"Категория": "Транспорт", "Дата операции": "01.11.2024 09:00:00", "Сумма платежа": -50},
        {"Категория": "Еда", "Дата операции": "01.12.2024 11:15:00", "Сумма платежа": -300},
        {"Категория": "Еда", "Дата операции": "05.12.2024 16:00:00", "Сумма платежа": -100},
        {"Категория": "Одежда", "Дата операции": "01.12.2024 18:00:00", "Сумма платежа": -500},
    ]
    return pd.DataFrame(data)
