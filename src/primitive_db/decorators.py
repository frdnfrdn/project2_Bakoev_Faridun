"""Декораторы и замыкания для улучшения кода."""

import time
from functools import wraps


def handle_db_errors(func):
    """Декоратор для централизованной обработки ошибок БД.

    Перехватывает FileNotFoundError, KeyError, ValueError
    и другие исключения, выводя понятные сообщения.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(
                f"Ошибка: Таблица или столбец {e} не найден."
            )
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
        return None
    return wrapper


def confirm_action(action_name):
    """Фабрика декораторов для подтверждения опасных операций.

    Перед выполнением функции запрашивает у пользователя
    подтверждение. Если ответ не 'y', операция отменяется.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f"Вы уверены, что хотите выполнить "
                f'"{action_name}"? [y/n]: '
            )
            if answer.strip().lower() == "y":
                return func(*args, **kwargs)
            print("Операция отменена.")
            return None
        return wrapper
    return decorator


def log_time(func):
    """Декоратор для замера времени выполнения функции.

    Использует time.monotonic() и выводит результат в консоль.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(
            f"Функция {func.__name__} выполнилась "
            f"за {elapsed:.3f} секунд."
        )
        return result
    return wrapper


def create_cacher():
    """Создать функцию кэширования через замыкание.

    Возвращает функцию cache_result(key, value_func), которая
    хранит кэш в замыкании. При повторном вызове с тем же ключом
    возвращает результат из кэша без вызова value_func.
    """
    cache = {}

    def cache_result(key, value_func):
        """Получить результат из кэша или вычислить и сохранить."""
        if key not in cache:
            result = value_func()
            if result is not None:
                cache[key] = result
            return result
        return cache[key]

    return cache_result
