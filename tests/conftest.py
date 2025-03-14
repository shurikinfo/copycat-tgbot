import os
from unittest.mock import AsyncMock, MagicMock

import dotenv
import pytest
from aiogram.types import Update
from fastapi import Request

from copycat_tgbot.app import App


@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    """Фикстура для установки переменных окружения на время всех тестов."""
    dotenv.load_dotenv()
    os.environ["CONFIG"] = "unittest"
    yield


@pytest.fixture(scope="session")
def app(set_env_vars):
    """Фикстура для создания экземпляра приложения."""
    app = App()
    app.init_app()
    return app
