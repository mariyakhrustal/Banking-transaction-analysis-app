from datetime import datetime

import pandas as pd


def read_greeting() -> str:
    """Функция для генерации приветствия пользователя"""
    current_time = datetime.now()
    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_file_xlsx(file_path: str) -> pd.DataFrame:
    """Функция читает данные из файла и возвращает DataFrame"""
    excel_data = pd.read_excel(file_path)
    return excel_data


def filter_transacts_by_card_number(df_transacts: pd.DataFrame) -> list[dict]:
    """
    Функция, которая возвращает:
    последние 4 цифры карты;
    общую сумму расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    """
    pass


if __name__ == '__main__':
    df = read_file_xlsx("../data/operations.xlsx")
    print(df.iloc[0])
