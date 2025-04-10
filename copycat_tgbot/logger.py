import logging

from copycat_tgbot.constants import LOGGER_FORMAT, LOGGER_LEVEL, LOGGER_STREAM


def init_logger(level: str = LOGGER_LEVEL) -> logging.Logger:
    """
    Определяем логер

    :param level: Уровень логирования
    :return:
    """

    logger = logging.getLogger()
    formatter = logging.Formatter(LOGGER_FORMAT)
    handler = logging.StreamHandler(LOGGER_STREAM)

    logger.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
