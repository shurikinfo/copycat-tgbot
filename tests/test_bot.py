import os

import pytest
from aiogram import types


@pytest.mark.asyncio
async def test_bot_initialization(app):
    """Тест инициализации бота."""
    assert app.bot.bot is not None
    assert app.bot.dp is not None
    assert app.bot.bot.token == os.getenv("BOT_TOKEN")


@pytest.mark.asyncio
async def test_start_command(app):
    message = types.Message(
        message_id=225,
        from_user=types.User(id=712319672, first_name="Alexander", is_bot=False),
        chat=types.Chat(id=712319672, type="private"),
        text="/start",
        date=1741193885,
    )

    await app.bot.dp._process_update(
        app.bot.bot, types.Update(update_id=1, message=message)
    )

    # Проверяем, что бот ответил
    assert len(app.bot.bot.method_calls) == 1
    assert app.bot.bot.method_calls[0][0] == "send_message"
    assert app.bot.bot.method_calls[0][1]["text"] == "Привет! Я тестовый бот."
