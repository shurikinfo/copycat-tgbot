from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from copycat_tgbot.constants import PROMT_AVAILABLE_ROUTES


start_router: Router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    message_promt = 'Привет!\n\nБот в вашем чате. Нижe список доступных команд:\n'
    message_promt += f'{PROMT_AVAILABLE_ROUTES}\n'
    message_promt += 'P.S. Список функций будет пополнятся в будущем'

    await message.answer(message_promt)