from pathlib import Path
from typing import Any

import pandas as pd


def read_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список транзакций из CSV-файла."""
    path = Path(file_path)

    try:
        dataframe = pd.read_csv(path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return []

    transactions: list[dict[str, Any]] = dataframe.to_dict(orient="records")

    return transactions


def read_transactions_from_excel(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список транзакций из Excel-файла."""
    path = Path(file_path)

    try:
        dataframe = pd.read_excel(path)
    except (FileNotFoundError, ValueError):
        return []

    transactions: list[dict[str, Any]] = dataframe.to_dict(orient="records")

    return transactions
