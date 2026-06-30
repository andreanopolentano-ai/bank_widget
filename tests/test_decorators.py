from pathlib import Path

import pytest

from src.decorators import log


def test_log_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует вывод лога в консоль при успешном выполнении функции."""

    @log()
    def add_numbers(x: int, y: int) -> int:
        return x + y

    result = add_numbers(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert captured.out == "add_numbers ok\n"


def test_log_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует вывод лога в консоль при ошибке функции."""

    @log()
    def divide_numbers(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 0)

    captured = capsys.readouterr()

    assert captured.out == "divide_numbers error: ZeroDivisionError. Inputs: (1, 0), {}\n"


def test_log_success_file(tmp_path: Path) -> None:
    """Тестирует запись лога в файл при успешном выполнении функции."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply_numbers(x: int, y: int) -> int:
        return x * y

    result = multiply_numbers(3, 4)

    assert result == 12
    assert log_file.read_text(encoding="utf-8") == "multiply_numbers ok\n"


def test_log_error_file(tmp_path: Path) -> None:
    """Тестирует запись лога в файл при ошибке функции."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def get_item(items: list[int], index: int) -> int:
        return items[index]

    with pytest.raises(IndexError):
        get_item([], 1)

    assert log_file.read_text(encoding="utf-8") == (
        "get_item error: IndexError. Inputs: ([], 1), {}\n"
    )


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (1, 2, 3),
        (10, 5, 15),
        (-1, 1, 0),
    ],
)
def test_log_with_parametrize(
    capsys: pytest.CaptureFixture[str],
    x: int,
    y: int,
    expected: int,
) -> None:
    """Тестирует декоратор с параметризацией."""

    @log()
    def add_numbers(first_number: int, second_number: int) -> int:
        return first_number + second_number

    result = add_numbers(x, y)
    captured = capsys.readouterr()

    assert result == expected
    assert captured.out == "add_numbers ok\n"
