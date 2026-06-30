from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [41428829, 939719570]),
        ("CANCELED", [594226727, 615064591]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(
    operations: list[dict[str, Any]],
    state: str,
    expected_ids: list[int],
) -> None:
    """Тестирует фильтрацию операций по статусу."""
    result = filter_by_state(operations, state)

    assert [operation["id"] for operation in result] == expected_ids


def test_filter_by_state_default_value(operations: list[dict[str, Any]]) -> None:
    """Тестирует фильтрацию по статусу EXECUTED по умолчанию."""
    result = filter_by_state(operations)

    assert [operation["id"] for operation in result] == [41428829, 939719570]


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [41428829, 615064591, 594226727, 939719570]),
        (False, [939719570, 594226727, 615064591, 41428829]),
    ],
)
def test_sort_by_date(
    operations: list[dict[str, Any]],
    reverse: bool,
    expected_ids: list[int],
) -> None:
    """Тестирует сортировку операций по дате."""
    result = sort_by_date(operations, reverse)

    assert [operation["id"] for operation in result] == expected_ids


def test_sort_by_date_with_same_dates() -> None:
    """Тестирует сортировку операций с одинаковыми датами."""
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T00:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-01T00:00:00.000000"},
    ]

    result = sort_by_date(operations)

    assert result == operations
