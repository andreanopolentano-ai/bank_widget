import re
from collections import Counter
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]],
    search: str,
) -> list[dict[str, Any]]:
    """Возвращает операции, в описании которых есть строка поиска."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [
        operation
        for operation in data
        if pattern.search(str(operation.get("description", "")))
    ]


def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Возвращает количество операций по заданным категориям."""
    descriptions = [
        str(operation.get("description", ""))
        for operation in data
    ]

    counter = Counter(descriptions)

    return {
        category: counter[category]
        for category in categories
    }
