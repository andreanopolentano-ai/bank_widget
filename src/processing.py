from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Возвращает список операций с указанным статусом."""
    filtered_operations = []

    for operation in operations:
        if operation.get("state") == state:
            filtered_operations.append(operation)

    return filtered_operations


def sort_by_date(
    operations: list[dict[str, Any]],
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Возвращает список операций, отсортированный по дате."""
    sorted_operations = sorted(
        operations,
        key=lambda operation: operation["date"],
        reverse=reverse,
    )

    return sorted_operations