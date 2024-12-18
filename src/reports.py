import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.decorators import report
from src.utils import read_file_xlsx

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)  # pragma: no cover

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(os.path.join(logs_dir, "reports.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


@report("../reports/report.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    logger.info("Начало работы функции траты по категориям")
    category = category.capitalize()
    if date:
        input_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    else:
        input_date = datetime.now()
    logger.info("Определение времени для работы с транзакциями")
    transactions["Дата операции"] = transactions["Дата операции"].apply(
        lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S") if pd.notnull(x) else None
    )
    three_month_ago = input_date - timedelta(days=90)
    filtered_df = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_month_ago)
        & (transactions["Дата операции"] <= input_date)
        & (transactions["Сумма платежа"] < 0)
    ]
    logger.info("Транзакции переводятся в список словарей для дальнейшей работы")
    transacts_dict = filtered_df.to_dict(orient="records")
    final_list = []
    for item in transacts_dict:
        item["Дата операции"] = item["Дата операции"].strftime("%d.%m.%Y %H:%M:%S")
        final_list.append(item)
    logger.info(f"Формирование итогового списка транзакций всего: {len(final_list)} транзакций")
    logger.info("Завершение работы функции. Формирование итоговой json строки")
    return json.dumps(final_list, ensure_ascii=False, indent=4)


if __name__ == "__main__":  # Пример использования
    df = read_file_xlsx("../data/operations.xlsx")
    print(spending_by_category(df, "медицина", "11.12.2021 00:00:00"))
