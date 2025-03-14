from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from copycat_tgbot.base import Context


class ContextMiddleware(BaseMiddleware):
    def __init__(self, context: Context) -> None:
        self.context = context

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        self.context.from_telegram_message(event)

        return await handler(event, data)
