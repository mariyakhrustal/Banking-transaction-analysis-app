import pytest

from src.services import investment_bank


def test_investment_bank():
    """Тестирование функции"""
    transactions = [
        {"Дата операции": "10.07.2023 00:00:00", "Сумма операции": 1500},
        {"Дата операции": "15.07.2023 00:00:00", "Сумма операции": 2500},
        {"Дата операции": "20.07.2023 00:00:00", "Сумма операции": 3200},
        {"Дата операции": "01.08.2023 00:00:00", "Сумма операции": 1300},
    ]
    month = "2023-07"
    limit = 500
    assert investment_bank(month, transactions, limit) == '{\n    "Сумма, отложенная в «Инвесткопилку»": 300.0\n}'


def test_invalid_month_format():
    """Тестирование функции, когда введен неправильный формат месяца"""
    transactions = []
    month = "2024/07"
    limit = 50
    with pytest.raises(ValueError):
        investment_bank(month, transactions, limit)


def test_no_transactions_in_month():
    """Тестирование функции, когда нет введенного в функцию месяца в структуре данных"""
    transactions = [{"Дата операции": "10.08.2024 00:00:00", "Сумма операции": 1712}]
    month = "2024-07"
    limit = 50
    assert investment_bank(month, transactions, limit) == '{\n    "Сумма, отложенная в «Инвесткопилку»": 0.0\n}'


def test_different_limits():
    """Тестирование функции с разными лимитами"""
    transactions = [
        {"Дата операции": "10.07.2024 00:00:00", "Сумма операции": 1712},
        {"Дата операции": "15.07.2024 00:00:00", "Сумма операции": 185},
        {"Дата операции": "20.07.2024 00:00:00", "Сумма операции": 499},
    ]
    month = "2024-07"
    assert investment_bank(month, transactions, 10) == '{\n    "Сумма, отложенная в «Инвесткопилку»": 14.0\n}'
    assert investment_bank(month, transactions, 100) == '{\n    "Сумма, отложенная в «Инвесткопилку»": 104.0\n}'


def test_raise_exception():
    transactions = [
        {"Дата операции": "10.07.2024 00:00:00"},
        {"Дата операции": "15.07.2024 00:00:00"},
        {"Дата операции": "20.07.2024 00:00:00"},
    ]
    month = "2024-07"
    assert investment_bank(month, transactions, 50) == "0.0"
