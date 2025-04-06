from aiogram.fsm.state import State, StatesGroup


class AddBook(StatesGroup):
    title = State()  # Шаг 1: Название книги
    author = State()  # Шаг 2: Автор книги
    year = State()  # Шаг 3: Год написания книги
    confirm = State()  # Шаг 4: Подтверждение
