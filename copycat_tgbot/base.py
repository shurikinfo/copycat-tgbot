import time
from typing import Any, Dict, Optional

from aiogram.types import Message


class Config(Dict[str, Any]):
    """Конфигурация приложения"""

    def __init__(self) -> None:
        self.is_loaded = False
        super().__init__()

    def load(self, config: Dict[str, Any]) -> None:
        """
        Загрузка словаря

        :param config: Словать конфигурации
        :return:
        """
        self.update(config)
        self.is_loaded = True

    def load_from_module(self, module_import_path: str) -> None:
        """
        Заполнить app.config настройками

        :param module_import_path: .py файл с конфигом, из которого нужно достать информацию
        :return:
        """

        _, tail = module_import_path.split(".", 1)
        conf_module = __import__(module_import_path, fromlist=[tail])
        self.load(conf_module.__dict__)


class Context:
    """Содержит информацию о текущем запросе"""

    __slots__ = (
        "message",
        "vars",
        "ts",
    )

    def __init__(self) -> None:
        self.message: Optional[Message] = None
        self.vars: Dict[str, Any] = {}
        self.ts: float = time.time()

    def get(self, key: str) -> Any:
        """
        Получение значения по ключу

        :param key: Название ключа
        :return:
        """
        if key in self.vars:
            return self.vars.get(key, None)

    def set(self, key: str, value: Any) -> None:
        """
        Добавление в контекст данных

        :param key: Название ключа
        :param value: Значение, которое нужно сохранить
        :return:
        """
        self.vars[key] = value

    @classmethod
    def from_telegram_message(cls, message: Message) -> None:
        """
        Обогатить контекст данными из сообщения от пользователя

        :param message: Объект Message из которого достанется информация
        :return:
        """
        cls.message = message
