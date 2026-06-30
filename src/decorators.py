from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def log(filename: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Логирует результат выполнения функции или возникшую ошибку."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """Оборачивает функцию логированием."""

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Выполняет функцию и записывает результат ее работы в лог."""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"
                _write_log(message, filename)
                return result
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. "
                    f"Inputs: {args}, {kwargs}\n"
                )
                _write_log(message, filename)
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: str | None = None) -> None:
    """Записывает сообщение в файл или выводит его в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message)
    else:
        print(message, end="")
