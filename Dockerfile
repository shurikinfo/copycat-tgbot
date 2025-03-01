FROM python:3.12 AS deps-image
#
WORKDIR /copycat_tgbot
# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем исходный код
COPY . .

# Команда для запуска скрипта
CMD ["poetry", "run", "run_bot"]
