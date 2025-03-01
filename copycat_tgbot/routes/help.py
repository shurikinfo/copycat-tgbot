from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from copycat_tgbot.constants import PROMT_AVAILABLE_ROUTES


help_router = Router()

@help_router.message(Command('help'))
async def start(message: Message):
    message_promt = 'Нижe список доступных команд:\n'
    message_promt += f'{PROMT_AVAILABLE_ROUTES}\n'
    message_promt += 'P.S. Список функций будет пополнятся в будущем'

    await message.answer(message_promt)