#!/bin/bash

# Значение по умолчанию для старого названия (в kebab-case)
DEFAULT_OLD_NAME_KEBAB="copycat-tgbot"
# Значение по умолчанию для старого названия (в snake_case)
DEFAULT_OLD_NAME_SNAKE="copycat_tgbot"

# Проверка на количество аргументов
if [ "$#" -ne 1 ]; then
    echo "Использование: $0 <новое_название>"
    echo "Пример: $0 newproject"
    exit 1
fi

# Функция для преобразования строки в kebab-case
to_kebab_case() {
    echo "$1" | sed -r 's/([A-Z])/-\1/g' | tr '[:upper:]' '[:lower:]' | sed 's/^-//'
}

# Функция для преобразования строки в snake_case
to_snake_case() {
    echo "$1" | sed -r 's/([A-Z])/_\1/g' | tr '[:upper:]' '[:lower:]' | sed 's/^_//'
}

# Новое название (переданное пользователем)
NEW_NAME=$1

# Преобразуем новое название в kebab-case и snake_case
NEW_NAME_KEBAB=$(to_kebab_case "$NEW_NAME")
NEW_NAME_SNAKE=$(to_snake_case "$NEW_NAME")

# Старые названия (по умолчанию)
OLD_NAME_KEBAB=$DEFAULT_OLD_NAME_KEBAB
OLD_NAME_SNAKE=$DEFAULT_OLD_NAME_SNAKE

# Получаем имя текущей папки (проекта)
CURRENT_DIR_NAME=$(basename "$PWD")

# Если текущая папка содержит старое название (kebab-case), переименовываем её
if [[ "$CURRENT_DIR_NAME" == *"$OLD_NAME_KEBAB"* ]]; then
    NEW_DIR_NAME=$(echo "$CURRENT_DIR_NAME" | sed "s/$OLD_NAME_KEBAB/$NEW_NAME_KEBAB/g")
    cd ..
    mv "$CURRENT_DIR_NAME" "$NEW_DIR_NAME"
    cd "$NEW_DIR_NAME"
    echo "Папка проекта переименована в '$NEW_DIR_NAME'."
fi

# Функция для замены названия в файлах и папках
replace_name() {
    local path=$1

    # Переименование файлов и папок (snake_case)
    find "$path" -depth -name "*$OLD_NAME_SNAKE*" | while read -r file; do
        new_file=$(echo "$file" | sed "s/$OLD_NAME_SNAKE/$NEW_NAME_SNAKE/g")
        mv "$file" "$new_file"
    done

    # Замена содержимого файлов (snake_case)
    find "$path" -type f -exec sed -i "s/$OLD_NAME_SNAKE/$NEW_NAME_SNAKE/g" {} +
}

# Запуск функции для текущей директории
replace_name "."

echo "Замена завершена!"
echo "Все вхождения '$OLD_NAME_KEBAB' (kebab-case) и '$OLD_NAME_SNAKE' (snake_case) заменены на '$NEW_NAME_KEBAB' и '$NEW_NAME_SNAKE' соответственно."