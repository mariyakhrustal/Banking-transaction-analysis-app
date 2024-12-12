import os
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from dotenv import load_dotenv
from pandas._libs.tslibs.timestamps import Timestamp

from src.utils import (filter_by_date_transacts, filter_transacts_by_card_number, get_conversion, get_stocks_prices,
                       get_top_transacts, read_file_xlsx, read_greeting)

load_dotenv()

currency_url = "https://api.apilayer.com/exchangerates_data/convert"
currency_api_key = os.getenv("CURRENCY_API_KEY")
headers = {"apikey": currency_api_key}


@pytest.mark.parametrize(
    "hour, expected",
    [
        (6, "Доброе утро"),
        (15, "Добрый день"),
        (21, "Добрый вечер"),
        (24, "Доброй ночи"),
    ],
)
def test_read_greeting(hour: int, expected: str) -> None:
    """Test gritting generation"""
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = hour
        assert read_greeting() == expected


@patch("pandas.read_excel", return_value=["mock_data_excel"])
def test_read_file_xlsx(mock_read_excel: MagicMock) -> None:
    """Test get excel data"""
    result = read_file_xlsx("mock_path.xlsx")
    assert result == ["mock_data_excel"]
    mock_read_excel.assert_called_once_with("mock_path.xlsx")


def test_read_file_xlsx_wrong_path() -> None:
    """Test get empty list from wrong path xlsx"""
    assert read_file_xlsx(" ") == []
    assert read_file_xlsx("1234") == []
    assert read_file_xlsx("example.xlsx") == []


@patch("requests.get")
def test_get_conversion_api_error(mock_get: MagicMock) -> None:
    """Тест с ошибкой в API-запросе (например, неверный ответ от сервера) при получении курса валют"""
    currencies = ["USD"]
    params = {"from": "USD", "to": "RUB", "amount": 1}
    mock_get.return_value.status_code = 500
    assert get_conversion(currencies) == []
    mock_get.assert_called_once_with(currency_url, headers=headers, params=params, timeout=30)


@patch("requests.get")
def test_get_conversion_exception(mock_get: MagicMock) -> None:
    """Тест на исключение при получении курса валют"""
    currencies = ["USD"]
    params = {"from": "USD", "to": "RUB", "amount": 1}
    mock_get.side_effect = Exception("test exception")
    assert get_conversion(currencies) == []
    mock_get.assert_called_once_with(currency_url, headers=headers, params=params, timeout=30)


@patch("requests.get")
def test_get_conversion_successful(mock_get: MagicMock) -> None:
    """Тест с валидной транзакцией при получении курса валют"""
    currencies = ["USD"]
    params = {"from": "USD", "to": "RUB", "amount": 1}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 60.0}
    assert get_conversion(currencies) == [{"currency": "USD", "rate": 60.0}]
    mock_get.assert_called_once_with(currency_url, headers=headers, params=params, timeout=30)


@patch("requests.get")
def test_get_stocks_prices_api_error(mock_get: MagicMock) -> None:
    """Тест с ошибкой в API-запросе (например, неверный ответ от сервера) при получении цены акций"""
    stocks = ["AAPL"]
    mock_get.return_value.status_code = 500
    assert get_stocks_prices(stocks) == []


@patch("requests.get")
def test_get_stocks_prices_exception(mock_get: MagicMock) -> None:
    """Тест на исключение при получении цены акций"""
    stocks = ["AAPL"]
    mock_get.side_effect = Exception("test exception")
    assert get_stocks_prices(stocks) == []


@patch("requests.get")
def test_get_stocks_prices_successful(mock_get: MagicMock) -> None:
    """Тест с валидной акцией при получении цены акций"""
    stocks = ["AAPL"]
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Global Quote": {"05. price": 100.0}}
    assert get_stocks_prices(stocks) == [{"price": 100.0, "stock": "AAPL"}]


def test_filter_transacts_by_card_number() -> None:
    """Проверка правильности фильтрации и расчетов"""
    data = {"Номер карты": ["1234567890123456", "0987654321098765"], "Сумма платежа": [-500, -200]}
    df = pd.DataFrame(data)
    expected = [
        {"last_digits": "8765", "total_spent": 200, "cashback": 2.0},
        {"last_digits": "3456", "total_spent": 500, "cashback": 5.0},
    ]
    result = filter_transacts_by_card_number(df)
    assert result == expected


def test_filter_transacts_by_card_number_error() -> None:
    """Проверка на ошибку фильтрации и расчетов"""
    data = {"Сумма платежа": [-500, -200]}
    df = pd.DataFrame(data)
    result = filter_transacts_by_card_number(df)
    assert result == []


def test_filter_by_date_transacts(sample_data: dict) -> None:
    end_date = "02.03.2019 12:00:00"
    test_df = pd.DataFrame(sample_data)
    result = filter_by_date_transacts(test_df, end_date)
    assert result.loc[0, "Сумма"] == 100
    assert result.loc[0, "Дата операции"] == Timestamp("2019-03-01 12:00:00")


def test_filter_by_date_transacts_error(sample_data: dict) -> None:
    end_date = "02.03.2019"
    test_df = pd.DataFrame(sample_data)
    result = filter_by_date_transacts(test_df, end_date)
    assert result == []


def test_get_top_transacts(sample_transact: pd.DataFrame) -> None:
    expected_result = [
        {"date": "04.01.2024", "amount": 3000, "category": "Путешествия", "description": "Отпуск"},
        {"date": "05.01.2024", "amount": 2500, "category": "Кафе", "description": "Обед"},
        {"date": "02.01.2024", "amount": 2000, "category": "Транспорт", "description": "Билет на автобус"},
        {"date": "03.01.2024", "amount": 1500, "category": "Развлечения", "description": "Кино"},
        {"date": "01.01.2024", "amount": 1000, "category": "Продукты", "description": "Покупка в магазине"},
    ]
    result = get_top_transacts(sample_transact)
    assert result == expected_result


def test_get_top_transacts_error(sample_data: dict) -> None:
    test_df = pd.DataFrame(sample_data)
    result = get_top_transacts(test_df)
    assert result == []


def test_get_top_transacts_less(sample_transact: pd.DataFrame) -> None:
    reduced_transactions = sample_transact.head(3)
    result = get_top_transacts(reduced_transactions)
    expected_result = [
        {"date": "02.01.2024", "amount": 2000, "category": "Транспорт", "description": "Билет на автобус"},
        {"date": "03.01.2024", "amount": 1500, "category": "Развлечения", "description": "Кино"},
        {"date": "01.01.2024", "amount": 1000, "category": "Продукты", "description": "Покупка в магазине"},
    ]
    assert result == expected_result
