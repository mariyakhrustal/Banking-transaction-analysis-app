import os
from functools import wraps
from typing import Any, Callable, Optional


def report(filename: Optional[str] = None) -> Callable:
    """Декоратор для записи отчета в файл"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            report_dir = "../reports"
            if filename:
                report_dir = os.path.dirname(filename)
                if report_dir and not os.path.exists(report_dir):
                    os.makedirs(report_dir)
            else:
                if not os.path.exists(report_dir):
                    os.makedirs(report_dir)
            try:
                result = func(*args, **kwargs)
                report_message = f"Результат функции {func.__name__}: {result}\n"
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(report_message)
                else:
                    with open(os.path.join(report_dir, "report.txt"), "w", encoding="utf-8") as file:
                        file.write(report_message)
                return result
            except Exception as error:
                report_message = f"{func.__name__} error: {error.__class__.__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(report_message)
                else:
                    with open(os.path.join(report_dir, "report.txt"), "w", encoding="utf-8") as file:
                        file.write(report_message)
        return wrapper
    return decorator
