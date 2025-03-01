import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

from copycat_tgbot.base import Config
from copycat_tgbot.logger import init_logger
from copycat_tgbot.routes.help import help_router
from copycat_tgbot.routes.start import start_router

logger = logging.getLogger(__name__)


class TgBot:
    def __init__(self):
        self.version = "1.0.1"
        self.logger = None
        self.dp = None
        self.bot = None
        self.config = Config()

    def init_app(self):
        config = getenv("CONFIG") or "dev"
        logger.debug(f"Выбран конфиг {config}")

        logger.debug(f"Загружаем конфиг {config}")
        self.config.load_from_module(f"copycat_tgbot.etc.{config}.config")

        logger.debug(f"Инициализируем логгер")
        if "LOG_LEVEL" in self.config:
            self.logger = init_logger(self.config["LOG_LEVEL"])
        else:
            self.logger = init_logger()

        logger.debug(f"Инициализируем root-роутер")
        self.dp = Dispatcher()

        logger.debug(f"Загружаем .env файл")
        try:
            env_file = find_dotenv(raise_error_if_not_found=True)
            load_dotenv(env_file)
            logger.debug(f"Загрузили .env файл: {env_file}")
        except OSError:
            logger.error(f".env файл не найден")
            exit(1)

        logger.debug(f"Инициализируем бота")
        self.bot = Bot(token=getenv("BOT_TOKEN"))

        logger.debug(f"Инициализируем команды")
        self.dp.include_routers(start_router, help_router)

    async def run(self):
        logger.debug(f"Запускаем бота")
        await self.dp.start_polling(self.bot)
