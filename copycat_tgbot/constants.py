# coding: utf-8
import logging
import sys

LOGGER_FORMAT = "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s"
LOGGER_LEVEL = logging.INFO
LOGGER_STREAM = sys.stdout

DEFAULT_TIMEZONE = "Europe/Moscow"

AVAILABLE_ROUTES = [
    {
        "name": "/help",
        "description": "Список доступных команд",
    }
]

PROMT_AVAILABLE_ROUTES = "".join(
    f"{route['name']} - {route['description']}\n" for route in AVAILABLE_ROUTES
)
