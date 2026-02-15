"""Модуль запуска, игровой цикл и обработка команд."""

import shlex

import prompt

from src.primitive_db.constants import META_FILEPATH
from src.primitive_db.core import (
    create_table,
    delete_records,
    display_records,
    drop_table,
    insert_record,
    list_tables,
    select_records,
    show_table_info,
    update_records,
)
from src.primitive_db.parser import (
    parse_delete_args,
    parse_insert_args,
    parse_select_args,
    parse_update_args,
)
from src.primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Вывести справочную информацию."""
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<зн1>, <зн2>, ...) - создать запись"
    )
    print(
        "<command> select from <имя_таблицы> "
        "[where <столбец> = <значение>] - прочитать записи"
    )
    print(
        "<command> update <имя_таблицы> set <стб> = <зн> "
        "where <стб> = <зн> - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> "
        "where <столбец> = <значение> - удалить запись"
    )
    print(
        "<command> info <имя_таблицы> - "
        "информация о таблице"
    )
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def _check_table_exists(metadata, table_name):
    """Проверить существование таблицы, вывести ошибку если нет."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    return True


def run():
    """Запустить основной цикл приложения."""
    print_help()

    while True:
        metadata = load_metadata(META_FILEPATH)
        user_input = prompt.string(">>>Введите команду: ")

        if user_input is None:
            continue

        user_input = user_input.strip()
        if not user_input:
            continue

        command = user_input.split()[0].lower()

        if command == "exit":
            break

        elif command == "help":
            print_help()

        elif command == "create_table":
            try:
                args = shlex.split(user_input)
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
                continue
            if len(args) < 3:
                print(
                    "Некорректное значение: недостаточно "
                    "аргументов. Попробуйте снова."
                )
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILEPATH, metadata)

        elif command == "drop_table":
            try:
                args = shlex.split(user_input)
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
                continue
            if len(args) < 2:
                print(
                    "Некорректное значение: не указано "
                    "имя таблицы. Попробуйте снова."
                )
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILEPATH, metadata)
            delete_table_data(table_name)

        elif command == "list_tables":
            list_tables(metadata)

        elif command == "insert":
            result = parse_insert_args(user_input)
            if result is None:
                print(
                    "Некорректный синтаксис команды insert. "
                    "Попробуйте снова."
                )
                continue
            table_name, values = result
            if not _check_table_exists(metadata, table_name):
                continue
            table_data = load_table_data(table_name)
            table_data = insert_record(
                metadata, table_name, values, table_data
            )
            save_table_data(table_name, table_data)

        elif command == "select":
            result = parse_select_args(user_input)
            if result is None:
                print(
                    "Некорректный синтаксис команды select. "
                    "Попробуйте снова."
                )
                continue
            table_name, where_clause = result
            if not _check_table_exists(metadata, table_name):
                continue
            table_data = load_table_data(table_name)
            records = select_records(table_data, where_clause)
            columns = metadata[table_name]["columns"]
            display_records(columns, records)

        elif command == "update":
            result = parse_update_args(user_input)
            if result is None:
                print(
                    "Некорректный синтаксис команды update. "
                    "Попробуйте снова."
                )
                continue
            table_name, set_clause, where_clause = result
            if not _check_table_exists(metadata, table_name):
                continue
            table_data = load_table_data(table_name)
            table_data, updated_ids = update_records(
                table_data, set_clause, where_clause
            )
            if updated_ids:
                for uid in updated_ids:
                    print(
                        f"Запись с ID={uid} в таблице "
                        f'"{table_name}" успешно обновлена.'
                    )
                save_table_data(table_name, table_data)
            else:
                print("Записи для обновления не найдены.")

        elif command == "delete":
            result = parse_delete_args(user_input)
            if result is None:
                print(
                    "Некорректный синтаксис команды delete. "
                    "Попробуйте снова."
                )
                continue
            table_name, where_clause = result
            if not _check_table_exists(metadata, table_name):
                continue
            table_data = load_table_data(table_name)
            table_data, deleted_ids = delete_records(
                table_data, where_clause
            )
            if deleted_ids:
                for did in deleted_ids:
                    print(
                        f"Запись с ID={did} успешно удалена "
                        f'из таблицы "{table_name}".'
                    )
                save_table_data(table_name, table_data)
            else:
                print("Записи для удаления не найдены.")

        elif command == "info":
            try:
                args = shlex.split(user_input)
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
                continue
            if len(args) < 2:
                print(
                    "Некорректное значение: не указано "
                    "имя таблицы. Попробуйте снова."
                )
                continue
            table_name = args[1]
            if not _check_table_exists(metadata, table_name):
                continue
            table_data = load_table_data(table_name)
            show_table_info(metadata, table_name, table_data)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
