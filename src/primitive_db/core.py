"""Основная логика работы с таблицами и данными."""

from src.primitive_db.constants import ID_COLUMN, ID_TYPE, VALID_TYPES


def create_table(metadata, table_name, columns):
    """Создать новую таблицу с указанными столбцами.

    Автоматически добавляет столбец ID:int в начало.
    Проверяет уникальность имени и корректность типов.
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = {ID_COLUMN: ID_TYPE}

    for col_def in columns:
        parts = col_def.split(":")
        if len(parts) != 2:
            print(f"Некорректное значение: {col_def}. Попробуйте снова.")
            return metadata

        col_name, col_type = parts

        if col_type not in VALID_TYPES:
            print(f"Некорректное значение: {col_type}. Попробуйте снова.")
            return metadata

        if col_name == ID_COLUMN:
            continue

        parsed_columns[col_name] = col_type

    metadata[table_name] = {"columns": parsed_columns}

    cols_str = ", ".join(
        f"{name}:{typ}" for name, typ in parsed_columns.items()
    )
    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {cols_str}"
    )

    return metadata


def drop_table(metadata, table_name):
    """Удалить таблицу из метаданных.

    Проверяет существование таблицы перед удалением.
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata):
    """Показать список всех таблиц."""
    if not metadata:
        print("Нет созданных таблиц.")
        return

    for table_name in metadata:
        print(f"- {table_name}")
