from pathlib import Path
from typing import Any
from unittest import mock
from unittest.mock import patch

from src.decorators import report


@report()
def multiply(a, b):
    return a * b


@report()
def divide(a, b):
    return a / b


@report(filename="test_error_report.txt")
def divide_func(a, b):
    return a / b


def test_report_exist_file_path_correct(tmp_path: Path):
    """Тест с введенным файлом успешный"""
    report_file = tmp_path / "reports" / "test.txt"

    @report(filename=str(report_file))
    def add_func(x: Any, y: Any) -> Any:
        return x + y

    add_func(6, 3)
    assert (tmp_path / "reports").exists()


def test_multiply_with_filename(tmp_path):
    report_file = tmp_path / "test_report.txt"

    @report(filename=str(report_file))
    def add_func(x: Any, y: Any) -> Any:
        return x + y

    add_func(6, 3)
    assert report_file.exists()
    with open(report_file, "r", encoding="utf-8") as file:
        report_content = file.read()
    assert "Результат функции add_func: 9\n" in report_content
    assert "error" not in report_content


def test_report_with_no_filename():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        result = multiply(7, 6)

        assert result == 42

        mock_file.assert_called_once_with("../reports\\report.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("Результат функции multiply: 42\n")


def test_function_error_report():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        result = divide_func(1, 0)

        assert result is None

        mock_file.assert_called_once_with("test_error_report.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("divide_func error: ZeroDivisionError. Inputs: (1, 0), {}\n")


def test_default_report_file():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        result = multiply(4, 5)

        assert result == 20

        mock_file.assert_called_once_with("../reports\\report.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("Результат функции multiply: 20\n")


def test_function_error_report_default_path():
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        result = divide(1, 0)

        assert result is None

        mock_file.assert_called_once_with("../reports\\report.txt", "w", encoding="utf-8")
        mock_file().write.assert_called_once_with("divide error: ZeroDivisionError. Inputs: (1, 0), {}\n")


@patch("os.makedirs")
@patch("os.path.exists")
def test_without_filename(mock_exists, mock_makedirs):
    mock_exists.return_value = False

    multiply(7, 6)

    # Проверка, что os.makedirs был вызван с дефолтным путем
    report_dir = "../reports"
    mock_makedirs.assert_called_once_with(report_dir)
