import logging
from os import getenv

from dotenv import find_dotenv, load_dotenv

from copycat_tgbot.base import Config
from copycat_tgbot.bot.app import TgBot
from copycat_tgbot.cache import RedisCache
from copycat_tgbot.error import GoogleError
from copycat_tgbot.http_clients.google.client import GoogleClient
from copycat_tgbot.logger import init_logger
from copycat_tgbot.server.app import Server

logger = logging.getLogger(__name__)


class App:
    """Основное приложение"""

    __slots__ = ("logger", "config", "bot", "server", "google", "cache")

    def __init__(self) -> None:
        self.logger = None
        self.bot = None
        self.config = None
        self.server = None
        self.google = None
        self.cache = None

    def init_app(self) -> None:
        self.config = Config()

        config = getenv("CONFIG") or "dev"
        logger.debug(f"Выбран конфиг {config}")

        logger.debug(f"Загружаем конфиг {config}")
        self.config.load_from_module(f"copycat_tgbot.etc.{config}.config")

        if not self.config.is_loaded:
            logger.error("Сначала загрузи конфиг")
            exit(1)

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

        logger.debug(f"Инициализируем кэш")
        self.cache = RedisCache(
            redis_host=self.config["REDIS_CACHE_CONF"].get("host"),
            redis_port=self.config["REDIS_CACHE_CONF"].get("port"),
            redis_db=self.config["REDIS_CACHE_CONF"].get("db"),
            default_ttl=self.config["DEFAULT_CACHE_TTL"],
        )

        logger.debug("Инициализируем GoogleClient")
        self.google = GoogleClient()
        self.google.init_client(self.config, self.cache)

        logger.debug("Настраиваем GoogleClient")
        try:
            self.google.setup_client()
        except GoogleError:
            # Без гугл-клиента нам не особо полезно приложение
            exit(1)

        logger.debug(f"Инициализируем бота")
        self.bot = TgBot(self.google)
        self.bot.init_app()
        logger.info("Бот инициализирован")

    def init_server(self) -> None:
        logger.debug(f"Инициализируем сервер")
        self.server = Server()
        self.server.init_app(self.bot, self.config)
        logger.info("Сервер инициализирован")
