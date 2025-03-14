import logging

from fastapi import FastAPI, Request

from copycat_tgbot.base import Config
from copycat_tgbot.bot.app import TgBot

logger = logging.getLogger(__name__)


class Server:
    """
    Сущность сервера
    Закрывать доступ ото всех, кроме IP-адресов Телеграмма и каких-то нужных стоит на уровне nginx
    Список адресов, с которых отправляет запросы Телеграмм: https://core.telegram.org/bots/webhooks
    """

    def __init__(self):
        self.app = None

    def init_app(self, bot: TgBot, config: Config) -> None:
        logger.debug("Инициализируем FastAPI")
        self.app = FastAPI()

        logger.debug("Регистрируем события ASGI")
        self.register_events(bot, config)

        logger.debug("Инициализируем роуты сервера")
        self.register_routers(bot)

    def register_events(self, bot: TgBot, config: Config) -> None:
        """
        Определяем события, которые нужно обработать

        :param bot: Сущность инициализированного бота
        :param config: Конфигурация приложения
        :return:
        """

        @self.app.on_event("startup")
        async def startup_event() -> None:
            """
            На включение сервера нужно прокинуть вебхук в бота, чтобы передавать ему запрос от Телеграмма
            :return:
            """
            await bot.on_startup(webhook_url=config.get("WEBHOOK_URL"))

        @self.app.on_event("shutdown")
        async def shutdown_event():
            """
            Уходя, гасите свет

            :return:
            """
            await bot.on_shutdown()

    def register_routers(self, bot: TgBot) -> None:
        """
        Определяем ручки, которые будет обрабатывать сервер

        :param bot: Сущность инициализированного бота
        :return:
        """

        @self.app.post("/webhook")
        async def webhook(request: Request) -> dict:
            # Передаем обновление в диспетчер
            await bot.webhook_handler(request)
            return {"status": "ok"}

        @self.app.get("/")
        async def root():
            return {"message": "Telegram Bot is running!"}
