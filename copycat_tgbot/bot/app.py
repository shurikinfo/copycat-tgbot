import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, Update
from fastapi import Request

from copycat_tgbot.base import Context
from copycat_tgbot.bot.middleware import ContextMiddleware
from copycat_tgbot.bot.routers.default import DefaultRouter

logger = logging.getLogger(__name__)


class TgBot:
    """
    Сущность Телеграм бота
    """

    def __init__(self):
        self.dp = None
        self.bot = None
        self.context = Context()
        self.commands = None

    def init_app(self):
        logger.debug(f"Инициализируем бота")
        self.bot = Bot(token=getenv("BOT_TOKEN"))

        logger.debug(f"Инициализируем Dispatcher")
        self.dp = Dispatcher(bot=self.bot)
        self.dp.message.middleware(ContextMiddleware(self.context))

        logger.debug(f"Инициализируем команды")

        default_router = DefaultRouter(self.dp)
        default_router.register_handlers()

        self.commands = default_router.get_commands()

    async def set_bot_commands(self):
        """Установка списка команд в боте"""

        await self.bot.set_my_commands(
            [BotCommand(command=cmd, description=desc) for cmd, desc in self.commands]
        )

    async def run(self):
        """Запуск бота в режиме long-poll"""

        logger.debug(f"Запускаем бота")
        await self.set_bot_commands()
        await self.dp.start_polling(self.bot)

    async def webhook_handler(self, request: Request):
        """
        Обработчик вебхука, в который Телеграм кидает свои запросы

        :param request: Запрос от Телеграмма
        :return:
        """
        await self.dp.feed_webhook_update(self.bot, Update(**await request.json()))

    async def on_startup(self, webhook_url: str):
        """
        Установка вебхука

        :param webhook_url: URL вебхука, в который отправляет запрос Телеграм
        :return:
        """
        webhook_info = await self.bot.get_webhook_info()
        if webhook_info.url != webhook_url:
            await self.bot.set_webhook(url=webhook_url)
        logger.debug(f"Бот запущен и вебхук установлен!: {webhook_info.url}")

    async def on_shutdown(self):
        """
        Удаление вебхука при остановке
        Уходя, тушите свет

        :return:
        """
        await self.bot.delete_webhook()
        logging.info(f"Вебхук удален.")
