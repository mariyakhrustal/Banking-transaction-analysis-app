import logging
import os
from functools import wraps
from typing import Any, Callable, Optional

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)  # pragma: no cover

logger = logging.getLogger("decorators")
file_handler = logging.FileHandler(os.path.join(logs_dir, "decorators.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def report(filename: Optional[str] = None) -> Callable:
    """Декоратор для записи отчета в файл"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info("Определение файла для декоратора")
            report_dir = "../reports"
            if filename:
                logger.info("Работа с переданным файлом для записи")
                report_dir = os.path.dirname(filename)
                if report_dir and not os.path.exists(report_dir):
                    os.makedirs(report_dir)
            else:
                logger.info("Работа с дефолтным файлом для записи")
                if not os.path.exists(report_dir):
                    os.makedirs(report_dir)
            try:
                logger.info("Вызов функции внутри декоратора")
                result = func(*args, **kwargs)
                report_message = f"Результат функции {func.__name__}: {result}\n"
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(report_message)
                else:
                    with open(os.path.join(report_dir, "report.log"), "w", encoding="utf-8") as file:
                        file.write(report_message)
                logger.info("Запись в файл результата успешной работы функции")
                return result
            except Exception as error:
                logger.info("Запись в файл об ошибке работы функции")
                report_message = f"{func.__name__} error: {error.__class__.__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(report_message)
                else:
                    with open(os.path.join(report_dir, "report.log"), "w", encoding="utf-8") as file:
                        file.write(report_message)
                logger.info("Завершение работы декоратора")

        return wrapper

    return decorator
