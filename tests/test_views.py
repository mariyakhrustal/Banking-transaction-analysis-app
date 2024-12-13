import json
from unittest import mock

from src.views import get_home_page_json_response


# Тест успешного выполнения функции
def test_get_home_page_json_response_success(mock_dependencies) -> None:
    # Мокаем данные в файле user_settings.json
    mock_open = mock.mock_open(
        read_data=json.dumps({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]})
    )

    with mock.patch("builtins.open", mock_open):
        response = get_home_page_json_response("2024-12-13")

    assert response == '{"greeting": "Hello, User!", "currency_rates": {"USD": 1.0}}'
    # Проверка, что все моки были вызваны
    mock_dependencies["mock_read_file_xlsx"].assert_called_once()
    mock_dependencies["mock_create_json_response"].assert_called_once()


# Тест на обработку ошибки FileNotFoundError
def test_get_home_page_json_response_file_not_found(mock_dependencies) -> None:
    # Мокаем FileNotFoundError
    mock_open = mock.mock_open(
        read_data=json.dumps({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]})
    )

    with mock.patch("builtins.open", mock_open):
        # Мокаем поведение, чтобы файл не был найден
        mock_open.side_effect = FileNotFoundError("user_settings.json not found")
        response = get_home_page_json_response("2024-12-13")

    assert response == []  # Функция должна вернуть пустой список при ошибке
    mock_dependencies["mock_read_file_xlsx"].assert_not_called()
