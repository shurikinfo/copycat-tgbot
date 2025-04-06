from copycat_tgbot.etc.config import *

REDIS_CACHE_CONF = {
    "host": "redis",
    "port": 6379,
    "db": 0,
    "password": CACHE_REDIS_PASSWORD or None,
}
