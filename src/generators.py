from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
) -> Iterator[dict[str, Any]]:
    """Возвращает итератор с транзакциями по заданной валюте."""
    for transaction in transactions:
        transaction_currency = (
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code")
        )

        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """Возвращает описания транзакций по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, stop + 1):
        card_number = f"{number:016d}"
        formatted_card_number = (
            f"{card_number[:4]} "
            f"{card_number[4:8]} "
            f"{card_number[8:12]} "
            f"{card_number[12:]}"
        )

        yield formatted_card_number
