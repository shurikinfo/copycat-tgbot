import asyncio

from copycat_tgbot.app import App

"""Тут запускаем бота"""
app = App()
app.init_app()

asyncio.run(app.bot.run())
