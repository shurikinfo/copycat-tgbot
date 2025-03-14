import itertools
import os
import string
from typing import Generator


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
