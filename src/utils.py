import json
from pathlib import Path
from typing import Any


def load_transactions_from_json(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список транзакций из JSON-файла."""
    path = Path(file_path)

    try:
        with path.open(encoding="utf-8") as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(transactions, list):
        return []

    return transactions
