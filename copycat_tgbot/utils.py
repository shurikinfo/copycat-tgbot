import itertools
import os
import string


def generate_excel_range(range_string: int) -> str:
    """
    Определить индекс столбца для Excel

    :param range_string: Длина данных, для которых хотим получить последний столбец
    :return: Буквенный индекс столбца (A, B, ..., ZY, ZZ)
    """
    return list(
        itertools.chain(
            string.ascii_uppercase,
            (
                "".join(pair)
                for pair in itertools.product(string.ascii_uppercase, repeat=2)
            ),
        )
    )[range_string - 1]


def env_to_dict(variables: set) -> dict:
    """
    Преобразует указанные переменные окружения в словарь.

    :param variables: Список имен переменных окружения.
    :return: Словарь, где ключи — имена переменных, а значения — их значения.
             Если переменная не существует, она не включается в словарь.
    """
    env_dict = {}

    for var in variables:
        if var in os.environ:  # Проверяем, существует ли переменная
            env_dict[var] = os.environ[var]
    return env_dict

def sheet_to_dict(values: list[list], use_first_row_as_headers: bool = True) -> dict:
    """
    Преобразует данные Sheets в dict

    :param values: Таблица
    :param use_first_row_as_headers: Использовать первую строку как заголовки
    :return: dict
    """

    headers = []
    data_start_row = 0

    if use_first_row_as_headers:
        headers = values[0]
        data_start_row = 1
    else:
        headers = [f"column{i + 1}" for i in range(len(values[0]))]

    data = []
    for row in values[data_start_row:]:
        row_data = {}
        for j in range(len(headers)):
            if j < len(row):
                row_data[headers[j]] = row[j]
            else:
                row_data[headers[j]] = None
        data.append(row_data)

    return {"data": data}


def find_dict_with_conditions(list_of_dicts, **conditions) -> dict | None:
    """
    Находит словарь по нескольким условиям

    :param list_of_dicts: Список словарей для поиска
    :param conditions: Пары ключ=значение для поиска
    :return: Найденный словарь или None, если не найден
    """
    for item in list_of_dicts:
        if all(item.get(k) == v for k, v in conditions.items()):
            return item
    return None
