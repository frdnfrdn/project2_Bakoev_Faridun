# Примитивная база данных

Консольное приложение на Python, имитирующее работу с базой данных. Поддерживает создание таблиц, CRUD-операции (insert, select, update, delete), фильтрацию по условиям и форматированный вывод.

## Установка

```bash
make install
```

Или напрямую:

```bash
poetry install
```

## Запуск

```bash
make project
```

Или напрямую:

```bash
poetry run project
```

## Управление таблицами

| Команда | Описание |
|---------|----------|
| `create_table <имя> <столбец1:тип> ...` | Создать таблицу (столбец ID добавляется автоматически) |
| `list_tables` | Показать список всех таблиц |
| `drop_table <имя>` | Удалить таблицу |
| `help` | Справочная информация |
| `exit` | Выйти из программы |

Поддерживаемые типы данных: `int`, `str`, `bool`.

### Пример использования

```
>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>>Введите команду: list_tables
- users

>>>Введите команду: drop_table users
Таблица "users" успешно удалена.

>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.
```

## Проверка кода

```bash
make lint
```

## Структура проекта

```
project2_Bakoev_Faridun/
├── src/
│   ├── __init__.py
│   └── primitive_db/
│       ├── __init__.py
│       ├── main.py          # Точка входа
│       ├── engine.py        # Игровой цикл и парсинг команд
│       ├── core.py          # Логика управления таблицами
│       ├── utils.py         # Работа с файлами (JSON)
│       └── constants.py     # Константы (пути, типы данных)
├── Makefile
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```
