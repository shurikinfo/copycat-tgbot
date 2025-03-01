import logging

from copycat_tgbot.constants import LOGGER_FORMAT, LOGGER_STREAM, LOGGER_LEVEL

def init_logger(level: str = LOGGER_LEVEL):
    # Определяем логгер

    logger = logging.getLogger()
    formatter = logging.Formatter(LOGGER_FORMAT)
    handler = logging.StreamHandler(LOGGER_STREAM)

    logger.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
