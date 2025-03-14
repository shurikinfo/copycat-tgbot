import logging

from aiogram import Dispatcher
from aiogram.types.message import Message

from copycat_tgbot.base import Context

logger = logging.getLogger(__name__)


class BaseRouter:
    """
    Базовый класс хэндлера команд бота
    """

    ROUTER_NAME = "base"

    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.commands = []  # Список поддерживаемых команд
        self.context = Context

    def register_handlers(self):
        """Метод для регистрации обработчиков."""
        raise NotImplementedError(
            "Метод register_handlers должен быть переопределен в дочернем классе"
        )

    def get_commands(self):
        """Возвращает список поддерживаемых команд."""
        return self.commands
