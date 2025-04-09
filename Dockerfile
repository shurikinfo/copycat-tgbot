FROM python:3.12 AS deps-image

RUN apt-get update && apt-get install -y curl

RUN mkdir /copycat_tgbot
WORKDIR /copycat_tgbot

FROM deps-image AS build-image

RUN apt-get update && \
    apt-get install -y \
    git \
    gcc \
    build-essential

# Устанавливаем Poetry
RUN pip install poetry==1.7.1

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install wheel && \
    poetry install

# Для запуска на бою
FROM deps-image


RUN mkdir -p /var/www/copycat_tgbot

COPY --from=build-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /var/www/copycat_tgbot
COPY  . .

ENTRYPOINT ["uvicorn"]

CMD ["copycat_tgbot.asgi:app.server.app", "--host", "0.0.0.0", "--log-level", "error"]