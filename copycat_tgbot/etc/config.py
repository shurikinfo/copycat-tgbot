from os import getenv

LOG_LEVEL = "INFO"
DEBUG = False
WEBHOOK_URL = getenv("WEBHOOK_URL")
DRIVE_URL = "https://www.googleapis.com/auth/drive"
SHEETS_URL = "https://www.googleapis.com/auth/spreadsheets"

# Конфиг Редиса для кеширования
CACHE_REDIS_PASSWORD = getenv("REDIS_PASSWORD")
REDIS_CACHE_CONF = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": CACHE_REDIS_PASSWORD or None,
}
DEFAULT_CACHE_TTL = 60 * 60 * 24  # на сутки
