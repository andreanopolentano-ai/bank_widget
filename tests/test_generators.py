from collections.abc import Iterator
from typing import Any

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
    expected_ids: list[int],
) -> None:
    """Тестирует фильтрацию транзакций по валюте."""
    result = filter_by_currency(transactions, currency)

    assert isinstance(result, Iterator)
    assert [transaction["id"] for transaction in result] == expected_ids


def test_filter_by_currency_empty_list() -> None:
    """Тестирует фильтрацию по валюте для пустого списка."""
    result = filter_by_currency([], "USD")

    assert list(result) == []


def test_transaction_descriptions(transactions: list[dict[str, Any]]) -> None:
    """Тестирует получение описаний транзакций."""
    descriptions = transaction_descriptions(transactions)

    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


def test_transaction_descriptions_empty_list() -> None:
    """Тестирует генератор описаний для пустого списка."""
    descriptions = transaction_descriptions([])

    with pytest.raises(StopIteration):
        next(descriptions)


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999999999999998,
            9999999999999999,
            [
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
        (
            3,
            3,
            [
                "0000 0000 0000 0003",
            ],
        ),
    ],
)
def test_card_number_generator(
    start: int,
    stop: int,
    expected: list[str],
) -> None:
    """Тестирует генерацию номеров карт в заданном диапазоне."""
    result = card_number_generator(start, stop)

    assert list(result) == expected


def test_card_number_generator_stop_iteration() -> None:
    """Тестирует корректное завершение генератора номеров карт."""
    generator = card_number_generator(1, 1)

    assert next(generator) == "0000 0000 0000 0001"

    with pytest.raises(StopIteration):
        next(generator)
