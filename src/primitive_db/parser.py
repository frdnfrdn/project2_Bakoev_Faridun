"""Парсер команд — разбор where, set и values."""


def parse_value(value_str):
    """Преобразовать строковое значение в Python-тип.

    Кавычки → str, true/false → bool, число → int, иначе → str.
    """
    value_str = value_str.strip()

    if not value_str:
        return None

    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False

    if (
        value_str.startswith('"') and value_str.endswith('"')
    ) or (
        value_str.startswith("'") and value_str.endswith("'")
    ):
        return value_str[1:-1]

    try:
        return int(value_str)
    except ValueError:
        pass

    return value_str


def parse_condition(condition_str):
    """Разобрать условие 'столбец = значение' в словарь.

    Пример: 'age = 28' → {'age': 28}
    """
    parts = condition_str.split("=", 1)
    if len(parts) != 2:
        return None
    col = parts[0].strip()
    val = parse_value(parts[1].strip())
    if not col or val is None:
        return None
    return {col: val}


def parse_insert_args(raw_input):
    """Разобрать команду insert.

    Формат: insert into <таблица> values (<зн1>, <зн2>, ...)
    Возвращает (table_name, [values]) или None.
    """
    lower = raw_input.lower()
    into_pos = lower.find("into ")
    values_pos = lower.find("values")

    if into_pos == -1 or values_pos == -1:
        return None

    table_name = raw_input[into_pos + 5:values_pos].strip()
    if not table_name:
        return None

    values_str = raw_input[values_pos + 6:].strip()
    if not (values_str.startswith("(") and values_str.endswith(")")):
        return None

    values_str = values_str[1:-1]
    raw_values = values_str.split(",")
    parsed = [parse_value(v) for v in raw_values]

    return table_name, parsed


def parse_select_args(raw_input):
    """Разобрать команду select.

    Формат: select from <таблица> [where <столбец> = <значение>]
    Возвращает (table_name, where_dict или None).
    """
    lower = raw_input.lower()
    from_pos = lower.find("from ")
    where_pos = lower.find(" where ")

    if from_pos == -1:
        return None

    if where_pos != -1:
        table_name = raw_input[from_pos + 5:where_pos].strip()
        where_str = raw_input[where_pos + 7:].strip()
        where_clause = parse_condition(where_str)
        if where_clause is None:
            return None
    else:
        table_name = raw_input[from_pos + 5:].strip()
        where_clause = None

    if not table_name:
        return None

    return table_name, where_clause


def parse_update_args(raw_input):
    """Разобрать команду update.

    Формат: update <таблица> set <стб> = <зн> where <стб> = <зн>
    Возвращает (table_name, set_dict, where_dict) или None.
    """
    lower = raw_input.lower()
    set_pos = lower.find(" set ")
    where_pos = lower.find(" where ")

    if set_pos == -1 or where_pos == -1:
        return None

    first_space = raw_input.find(" ")
    table_name = raw_input[first_space + 1:set_pos].strip()

    set_str = raw_input[set_pos + 5:where_pos].strip()
    where_str = raw_input[where_pos + 7:].strip()

    set_clause = parse_condition(set_str)
    where_clause = parse_condition(where_str)

    if not table_name or set_clause is None or where_clause is None:
        return None

    return table_name, set_clause, where_clause


def parse_delete_args(raw_input):
    """Разобрать команду delete.

    Формат: delete from <таблица> where <столбец> = <значение>
    Возвращает (table_name, where_dict) или None.
    """
    lower = raw_input.lower()
    from_pos = lower.find("from ")
    where_pos = lower.find(" where ")

    if from_pos == -1 or where_pos == -1:
        return None

    table_name = raw_input[from_pos + 5:where_pos].strip()
    where_str = raw_input[where_pos + 7:].strip()
    where_clause = parse_condition(where_str)

    if not table_name or where_clause is None:
        return None

    return table_name, where_clause
