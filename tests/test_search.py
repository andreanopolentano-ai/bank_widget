from typing import Any

from src.search import process_bank_operations, process_bank_search


def test_process_bank_search_found() -> None:
    """Тестирует поиск операций по описанию."""
    operations: list[dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]

    result = process_bank_search(operations, "перевод")

    assert result == [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
    ]


def test_process_bank_search_not_found() -> None:
    """Тестирует поиск операций без совпадений."""
    operations: list[dict[str, Any]] = [
        {"description": "Открытие вклада"},
    ]

    result = process_bank_search(operations, "перевод")

    assert result == []


def test_process_bank_search_empty_description() -> None:
    """Тестирует поиск по операции без описания."""
    operations: list[dict[str, Any]] = [
        {"id": 1},
    ]

    result = process_bank_search(operations, "перевод")

    assert result == []


def test_process_bank_search_uses_regex_case_insensitive() -> None:
    """Тестирует поиск с использованием регулярных выражений без учета регистра."""
    operations: list[dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]

    result = process_bank_search(operations, "ПЕРЕВОД")

    assert result == [
        {"description": "Перевод организации"},
    ]


def test_process_bank_operations() -> None:
    """Тестирует подсчет операций по категориям."""
    operations: list[dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]
    categories = [
        "Перевод организации",
        "Открытие вклада",
        "Перевод с карты на карту",
    ]

    result = process_bank_operations(operations, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
        "Перевод с карты на карту": 0,
    }


def test_process_bank_operations_empty_list() -> None:
    """Тестирует подсчет категорий по пустому списку операций."""
    result = process_bank_operations([], ["Перевод организации"])

    assert result == {
        "Перевод организации": 0,
    }


def test_process_bank_operations_missing_description() -> None:
    """Тестирует подсчет категорий при отсутствии описания в операции."""
    operations: list[dict[str, Any]] = [
        {"id": 1},
        {"description": "Открытие вклада"},
    ]

    result = process_bank_operations(operations, ["Открытие вклада"])

    assert result == {
        "Открытие вклада": 1,
    }
