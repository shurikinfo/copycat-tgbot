class BaseError(Exception):
    """Базовый класс для ошибок приложения"""

    message = "error"
    code = 10

    def __init__(self, message: str | None = None, code: int | None = None):
        self.message = message
        self.code = code


class TelegramError(BaseError):
    """Базовый класс для ошибок Telegram"""

    message = "Telegram error"
    code = 50


class TelegramInvalidToken(TelegramError):
    message = "Telegram invalid token"
    code = 51


class GoogleError(BaseError):
    """Базоый класс для ошибок Google-клиента"""

    message = "Google error"
    code = 100
