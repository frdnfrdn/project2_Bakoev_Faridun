"""Модуль запуска, игровой цикл и обработка команд."""

import shlex

import prompt

from src.primitive_db.constants import META_FILEPATH
from src.primitive_db.core import create_table, drop_table, list_tables
from src.primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Вывести справочную информацию."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Запустить основной цикл приложения."""
    print_help()

    while True:
        metadata = load_metadata(META_FILEPATH)
        user_input = prompt.string(">>>Введите команду: ")

        if user_input is None:
            continue

        try:
            args = shlex.split(user_input.strip())
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0].lower()

        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "create_table":
            if len(args) < 3:
                print(
                    "Некорректное значение: недостаточно аргументов. "
                    "Попробуйте снова."
                )
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILEPATH, metadata)
        elif command == "drop_table":
            if len(args) < 2:
                print(
                    "Некорректное значение: не указано имя таблицы. "
                    "Попробуйте снова."
                )
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILEPATH, metadata)
        elif command == "list_tables":
            list_tables(metadata)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
