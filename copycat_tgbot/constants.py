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

# Настройка логирования для Uvicorn
UVICORN_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOGGER_FORMAT,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
