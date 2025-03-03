import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import Request

from copycat_tgbot.bot.routers import routers

logger = logging.getLogger(__name__)


class TgBot:
    def __init__(self):
        self.dp = None
        self.bot = None

    def init_app(self):

        logger.debug(f"Инициализируем Dispatcher")
        self.dp = Dispatcher()

        logger.debug(f"Инициализируем бота")
        self.bot = Bot(token=getenv("BOT_TOKEN"))

        logger.debug(f"Инициализируем команды")
        self.dp.include_routers(*routers)

    async def run(self):
        logger.debug(f"Запускаем бота")
        await self.dp.start_polling(self.bot)

    async def webhook_handler(self, request: Request):
        await self.dp.feed_webhook_update(self.bot, Update(**await request.json()))

    # Установка вебхука
    async def on_startup(self, webhook_url: str):
        webhook_info = await self.bot.get_webhook_info()
        if webhook_info.url != webhook_url:
            await self.bot.set_webhook(url=webhook_url)
        logger.info(f"Бот запущен и вебхук установлен!: {webhook_info.url}")

    # Удаление вебхука при остановке
    async def on_shutdown(self):
        await self.bot.delete_webhook()
        logging.info(f"Вебхук удален.")
