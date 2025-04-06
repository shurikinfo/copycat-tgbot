import logging

from aiogram import Dispatcher

from copycat_tgbot.base import Context
from copycat_tgbot.http_clients.google.client import GoogleClient

logger = logging.getLogger(__name__)


class BaseRouter:
    """
    Базовый класс хэндлера команд бота
    """

    ROUTER_NAME = "base"

    def __init__(self, dp: Dispatcher, gc: GoogleClient | None = None):
        self.dp = dp
        self.commands = []  # Список поддерживаемых команд
        self.context = Context
        self.gc = gc  # Google Client

    def register_handlers(self):
        """Метод для регистрации обработчиков."""
        raise NotImplementedError(
            "Метод register_handlers должен быть переопределен в дочернем классе"
        )

    def get_commands(self):
        """Возвращает список поддерживаемых команд."""
        return self.commands
