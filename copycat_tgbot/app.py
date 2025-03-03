import logging
from os import getenv

from dotenv import find_dotenv, load_dotenv

from copycat_tgbot.base import Config
from copycat_tgbot.bot.app import TgBot
from copycat_tgbot.logger import init_logger
from copycat_tgbot.server.app import Server

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self.logger = None
        self.bot = None
        self.config = None
        self.server = None

    def init_app(self):
        self.config = Config()

        config = getenv("CONFIG") or "dev"
        logger.debug(f"Выбран конфиг {config}")

        logger.debug(f"Загружаем конфиг {config}")
        self.config.load_from_module(f"copycat_tgbot.etc.{config}.config")

        logger.debug(f"Инициализируем логгер")
        if "LOG_LEVEL" in self.config:
            self.logger = init_logger(self.config["LOG_LEVEL"])
        else:
            self.logger = init_logger()

        logger.debug(f"Загружаем .env файл")
        try:
            env_file = find_dotenv(raise_error_if_not_found=True)
            load_dotenv(env_file)
            logger.debug(f"Загрузили .env файл: {env_file}")
        except OSError:
            logger.error(f".env файл не найден")
            exit(1)

        logger.debug(f"Инициализируем бота")
        self.bot = TgBot()
        self.bot.init_app()

    def init_server(self):
        logger.debug(f"Инициализируем сервер")
        self.server = Server()
        self.server.init_app(self.bot)
