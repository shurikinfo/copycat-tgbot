import json
import logging
from datetime import timedelta

from redis import Redis

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(
        self, redis_host: str, redis_port: int, redis_db: int, default_ttl: int = 3600
    ):
        """
        Инициализация кэша.

        :param redis_host: Хост Redis
        :param redis_port: Порт Redis
        :param redis_db: Номер базы данных Redis
        :param default_ttl: Дефолтное время хранения кэша
        """
        self.redis_client = Redis(host=redis_host, port=redis_port, db=redis_db)
        self.default_ttl = default_ttl

    @staticmethod
    def _get_cache_key(func_name, *args, **kwargs) -> str:
        """
        Формирует уникальный ключ для кэша на основе имени функции и её аргументов.

        :param func_name: Имя функции
        :param args: Аргументы функции
        :param kwargs: Ключевые аргументы функции
        :return: Уникальный ключ для кэша
        """
        return f"{func_name}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"

    def cached(self, ttl_minutes: int = None):
        """
        Декоратор для кэширования результатов функции в Redis.

        :param ttl_minutes: Время жизни кэша в минутах
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                cache_key = self._get_cache_key(func.__name__, *args, **kwargs)
                # Пытаемся получить данные из кэша
                cached_response = self.redis_client.get(cache_key)

                if cached_response:
                    logger.debug("Данные получены из кэша")
                    return json.loads(cached_response)

                # Если данных в кэше нет, выполняем функцию
                logger.debug("Данные загружаются из API")
                result = func(*args, **kwargs)

                # Сохраняем результат в Redis с TTL
                self.redis_client.setex(
                    cache_key,
                    timedelta(minutes=ttl_minutes or self.default_ttl),
                    json.dumps(result),
                )
                logger.debug(f"Записали результат в кэш с ключом: {cache_key}")
                return result

            return wrapper

        return decorator

    def invalidate_cache(self, func_name, *args, **kwargs) -> None:
        """
        Удаляет кэш по указанному ключу.

        :param func_name: Имя функции
        :param args: Аргументы функции
        :param kwargs: Ключевые аргументы функции
        """
        cache_key = self._get_cache_key(func_name, *args, **kwargs)
        self.redis_client.delete(cache_key)
        logger.debug(f"Кэш с ключом {cache_key} удалён")
