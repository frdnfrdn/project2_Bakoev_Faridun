"""Вспомогательные функции для работы с файлами."""

import json
import os

from src.primitive_db.constants import DATA_DIR, DATA_FILE_EXT, FILE_ENCODING


def load_metadata(filepath):
    """Загрузить метаданные из JSON-файла.

    Если файл не найден, возвращает пустой словарь.
    """
    try:
        with open(filepath, "r", encoding=FILE_ENCODING) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохранить метаданные в JSON-файл."""
    with open(filepath, "w", encoding=FILE_ENCODING) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_table_data(table_name):
    """Загрузить данные таблицы из data/<table_name>.json.

    Если файл не найден, возвращает пустой список.
    """
    filepath = os.path.join(
        DATA_DIR, f"{table_name}{DATA_FILE_EXT}"
    )
    try:
        with open(filepath, "r", encoding=FILE_ENCODING) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохранить данные таблицы в data/<table_name>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(
        DATA_DIR, f"{table_name}{DATA_FILE_EXT}"
    )
    with open(filepath, "w", encoding=FILE_ENCODING) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def delete_table_data(table_name):
    """Удалить файл данных таблицы."""
    filepath = os.path.join(
        DATA_DIR, f"{table_name}{DATA_FILE_EXT}"
    )
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
