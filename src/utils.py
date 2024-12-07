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
    carts_dict = (
        df_transacts.loc[(df_transacts["Сумма платежа"] < 0)]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    cart_info = []
    for cart_num, sum_of_spent in carts_dict.items():
        total_spent = abs(sum_of_spent)
        cart_info.append(
            {"last_digits": {cart_num[-4:]},
             "total_spent": {total_spent},
             "cashback": {round(total_spent / 100, 2)}}
        )
    return cart_info


# if __name__ == '__main__':
    # df = read_file_xlsx("../data/operations.xlsx")
    # print(filter_transacts_by_card_number(df))
