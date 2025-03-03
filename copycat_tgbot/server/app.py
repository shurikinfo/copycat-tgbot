import logging
from os import getenv

from fastapi import FastAPI, Request

from copycat_tgbot.app import TgBot

logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        self.app = None

    def init_app(self, bot: TgBot):
        logger.debug("Инициализируем FastAPI")
        self.app = FastAPI()

        logger.debug("Регистрируем события ASGI")
        self.register_events(bot)

        logger.debug("Инициализируем роуты сервера")
        self.register_routers(bot)

    def register_events(self, bot: TgBot):
        @self.app.on_event("startup")
        async def startup_event():
            await bot.on_startup(webhook_url=getenv("WEBHOOK_URL"))

        @self.app.on_event("shutdown")
        async def shutdown_event():
            await bot.on_shutdown()

    def register_routers(self, bot: TgBot):
        @self.app.post("/webhook")
        async def webhook(request: Request):
            # Передаем обновление в диспетчер
            await bot.webhook_handler(request)
            return {"status": "ok"}

        @self.app.get("/")
        async def root():
            return {"message": "Telegram Bot is running!"}
