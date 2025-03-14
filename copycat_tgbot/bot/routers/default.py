from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from copycat_tgbot.bot.routers.base import BaseRouter
from copycat_tgbot.constants import PROMT_AVAILABLE_ROUTES


class DefaultRouter(BaseRouter):
    """
    Роутер для базовых команд
    """

    ROUTER_NAME = "default"

    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        self.commands = [
            ("start", "Запустить бота"),
            ("help", "Помощь"),
        ]

    def register_handlers(self):
        @self.dp.message(Command("help"))
        async def help_command(message: Message):

            message_promt = "Нижe список доступных команд:\n"
            message_promt += f"{PROMT_AVAILABLE_ROUTES}\n"
            message_promt += "P.S. Список функций будет пополнятся в будущем"

            await message.answer(message_promt)

        @self.dp.message(CommandStart())
        async def start_command(message: Message):
            message_promt = "Привет!\n\nБот в вашем чате."

            await message.answer(message_promt)
