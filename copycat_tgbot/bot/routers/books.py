from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from copycat_tgbot.bot.routers.base import BaseRouter


class BooksRouter(BaseRouter):
    """
    Роутер для книг
    """

    ROUTER_NAME = "books"

    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        self.commands = [
            ("addbook", "Добавить книгу"),
            ("getbooks", "Получить список книг"),
        ]

    def register_handlers(self):
        @self.dp.message(Command("addbook"))
        async def addbook_command(message: Message):

            message_promt = "Нижe список доступных команд:\n"
            message_promt += f"{PROMT_AVAILABLE_ROUTES}\n"
            message_promt += "P.S. Список функций будет пополнятся в будущем"

            await message.answer(message_promt)

        @self.dp.message(CommandStart())
        async def start_command(message: Message):
            message_promt = "Привет!\n\nБот в вашем чате."

            await message.answer(message_promt)
