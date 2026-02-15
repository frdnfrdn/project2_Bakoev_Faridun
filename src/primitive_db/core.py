"""Основная логика работы с таблицами и данными."""

from prettytable import PrettyTable

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


def _validate_type(value, expected_type):
    """Проверить соответствие значения ожидаемому типу."""
    if expected_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "str":
        return isinstance(value, str)
    if expected_type == "bool":
        return isinstance(value, bool)
    return False


def _generate_id(table_data):
    """Сгенерировать новый уникальный ID."""
    if not table_data:
        return 1
    return max(record[ID_COLUMN] for record in table_data) + 1


def _filter_records(table_data, where_clause):
    """Отфильтровать записи по условию where."""
    results = []
    for record in table_data:
        match = all(
            col in record and record[col] == val
            for col, val in where_clause.items()
        )
        if match:
            results.append(record)
    return results


def insert_record(metadata, table_name, values, table_data):
    """Добавить новую запись в таблицу.

    Проверяет существование таблицы, количество и типы значений.
    Генерирует ID автоматически.
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name]["columns"]
    data_columns = {
        k: v for k, v in columns.items() if k != ID_COLUMN
    }

    if len(values) != len(data_columns):
        print(
            f"Ошибка: Ожидается {len(data_columns)} значений, "
            f"получено {len(values)}."
        )
        return table_data

    col_items = list(data_columns.items())
    for i, (col_name, col_type) in enumerate(col_items):
        if not _validate_type(values[i], col_type):
            print(
                f"Некорректное значение: {values[i]} "
                f'для столбца "{col_name}" (ожидается {col_type}).'
            )
            return table_data

    new_id = _generate_id(table_data)
    record = {ID_COLUMN: new_id}
    for i, (col_name, _) in enumerate(col_items):
        record[col_name] = values[i]

    table_data.append(record)
    print(
        f'Запись с ID={new_id} успешно добавлена '
        f'в таблицу "{table_name}".'
    )

    return table_data


def select_records(table_data, where_clause=None):
    """Выбрать записи, опционально с фильтрацией по where."""
    if where_clause is None:
        return list(table_data)
    return _filter_records(table_data, where_clause)


def update_records(table_data, set_clause, where_clause):
    """Обновить записи, соответствующие условию where."""
    updated_ids = []
    for record in table_data:
        match = all(
            col in record and record[col] == val
            for col, val in where_clause.items()
        )
        if match:
            for col, val in set_clause.items():
                record[col] = val
            updated_ids.append(record.get(ID_COLUMN))

    return table_data, updated_ids


def delete_records(table_data, where_clause):
    """Удалить записи, соответствующие условию where."""
    deleted_ids = []
    new_data = []

    for record in table_data:
        match = all(
            col in record and record[col] == val
            for col, val in where_clause.items()
        )
        if match:
            deleted_ids.append(record.get(ID_COLUMN))
        else:
            new_data.append(record)

    return new_data, deleted_ids


def display_records(columns, records):
    """Вывести записи в формате PrettyTable."""
    if not records:
        print("Записи не найдены.")
        return

    table = PrettyTable()
    table.field_names = list(columns.keys())
    for record in records:
        table.add_row([record.get(col, "") for col in columns])
    print(table)


def show_table_info(metadata, table_name, table_data):
    """Вывести информацию о таблице."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]["columns"]
    cols_str = ", ".join(
        f"{name}:{typ}" for name, typ in columns.items()
    )

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {cols_str}")
    print(f"Количество записей: {len(table_data)}")
