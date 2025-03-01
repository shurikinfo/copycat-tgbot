import asyncio
from copycat_tgbot.app import TgBot

"""Тут запускаем бота"""
app = TgBot()
app.init_app()
asyncio.run(app.run())