from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from dateutil.parser import parse

from copycat_tgbot.bot.routers.base import BaseRouter
from copycat_tgbot.bot.states.books import AddBook
from copycat_tgbot.http_clients.google.client import GoogleClient
from copycat_tgbot.http_clients.google.model import BookModel


class BooksRouter(BaseRouter):
    """
    Роутер для книг
    """

    ROUTER_NAME = "books"

    def __init__(self, dp: Dispatcher, gc: GoogleClient):
        super().__init__(dp, gc)
        self.commands = [("addbook", "Добавить книгу")]

    def register_handlers(self):
        @self.dp.message(Command("addbook"))
        async def addbook_command(message: Message, state: FSMContext) -> None:
            await state.set_state(AddBook.title)
            await message.answer(
                "Как называется книга?",
                reply_markup=ReplyKeyboardRemove(),
            )

        @self.dp.message(AddBook.title)
        async def process_title(message: Message, state: FSMContext) -> None:
            await state.update_data(title=message.text)
            await state.set_state(AddBook.author)
            await message.answer(
                "Кто автор книги?",
                reply_markup=ReplyKeyboardRemove(),
            )

        @self.dp.message(AddBook.author)
        async def process_author(message: Message, state: FSMContext) -> None:
            await state.update_data(author=message.text)
            await state.set_state(AddBook.year)
            await message.answer(
                "Когда была написана книга?",
                reply_markup=ReplyKeyboardRemove(),
            )

        @self.dp.message(AddBook.year)
        async def process_year(message: Message, state: FSMContext) -> None:
            try:
                date = parse(message.text, fuzzy=True).year
            except Exception:
                date = None

            if not date:
                await state.set_state(AddBook.year)
                await message.answer(
                    "Не корректно указан год. Укажите правильный (1-9999)",
                    reply_markup=ReplyKeyboardRemove(),
                )
            else:
                data = await state.update_data(year=message.text)
                summary = (
                    "Проверь свои данные:\n"
                    f"Книга: {data['title']}\n"
                    f"Автор: {data['author']}\n"
                    f"Год: {data['year']}\n\n"
                    "Всё верно? (Да/Нет)"
                )
                await state.set_state(AddBook.confirm)
                await message.answer(
                    text=summary,
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Да"),
                                KeyboardButton(text="Нет"),
                            ]
                        ],
                        resize_keyboard=True,
                    ),
                )

        @self.dp.message(AddBook.confirm)
        async def process_confirm(message: Message, state: FSMContext) -> None:
            data = await state.get_data()
            if message.text.lower() == "нет":
                await state.clear()
                await message.answer(
                    "В таком случае, начни заново",
                    reply_markup=ReplyKeyboardRemove(),
                )
            elif message.text.lower() == "да":
                self.gc.sheets.append_to_sheet(
                    values=[
                        list(
                            BookModel(
                                data["title"], data["author"], data["year"]
                            ).__dict__.values()
                        )
                    ],
                    sheet_title="books",
                )
                await message.answer(
                    "Отлично. Сохранил себе эту книгу",
                    reply_markup=ReplyKeyboardRemove(),
                )
