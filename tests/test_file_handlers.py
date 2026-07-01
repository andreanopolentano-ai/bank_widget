from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import pandas as pd

from src.file_handlers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


def test_read_transactions_from_csv_success() -> None:
    """Тестирует успешное чтение транзакций из CSV-файла."""
    dataframe = pd.DataFrame(
        [
            {"id": 1, "state": "EXECUTED", "amount": 1000},
            {"id": 2, "state": "CANCELED", "amount": 500},
        ]
    )

    with patch("src.file_handlers.pd.read_csv", return_value=dataframe) as mock_read_csv:
        result = read_transactions_from_csv("data/transactions.csv")

    assert result == [
        {"id": 1, "state": "EXECUTED", "amount": 1000},
        {"id": 2, "state": "CANCELED", "amount": 500},
    ]
    mock_read_csv.assert_called_once_with(Path("data/transactions.csv"))


def test_read_transactions_from_csv_file_not_found() -> None:
    """Тестирует чтение несуществующего CSV-файла."""
    with patch("src.file_handlers.pd.read_csv", side_effect=FileNotFoundError):
        result = read_transactions_from_csv("data/transactions.csv")

    assert result == []


def test_read_transactions_from_csv_empty_file() -> None:
    """Тестирует чтение пустого CSV-файла."""
    with patch(
        "src.file_handlers.pd.read_csv",
        side_effect=pd.errors.EmptyDataError("No columns to parse from file"),
    ):
        result = read_transactions_from_csv("data/transactions.csv")

    assert result == []


def test_read_transactions_from_csv_returns_list_of_dicts() -> None:
    """Тестирует тип результата при чтении CSV-файла."""
    dataframe = pd.DataFrame([{"id": 1}, {"id": 2}])

    with patch("src.file_handlers.pd.read_csv", return_value=dataframe):
        result: list[dict[str, Any]] = read_transactions_from_csv(
            "data/transactions.csv"
        )

    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)


def test_read_transactions_from_excel_success() -> None:
    """Тестирует успешное чтение транзакций из Excel-файла."""
    dataframe = pd.DataFrame(
        [
            {"id": 1, "state": "EXECUTED", "amount": 1000},
            {"id": 2, "state": "CANCELED", "amount": 500},
        ]
    )

    with patch(
        "src.file_handlers.pd.read_excel",
        return_value=dataframe,
    ) as mock_read_excel:
        result = read_transactions_from_excel("data/transactions_excel.xlsx")

    assert result == [
        {"id": 1, "state": "EXECUTED", "amount": 1000},
        {"id": 2, "state": "CANCELED", "amount": 500},
    ]
    mock_read_excel.assert_called_once_with(Path("data/transactions_excel.xlsx"))


def test_read_transactions_from_excel_file_not_found() -> None:
    """Тестирует чтение несуществующего Excel-файла."""
    with patch("src.file_handlers.pd.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_from_excel("data/transactions_excel.xlsx")

    assert result == []


def test_read_transactions_from_excel_wrong_file() -> None:
    """Тестирует обработку некорректного Excel-файла."""
    with patch("src.file_handlers.pd.read_excel", side_effect=ValueError):
        result = read_transactions_from_excel("data/transactions_excel.xlsx")

    assert result == []


def test_read_transactions_from_excel_returns_list_of_dicts() -> None:
    """Тестирует тип результата при чтении Excel-файла."""
    dataframe = pd.DataFrame([{"id": 1}, {"id": 2}])

    with patch("src.file_handlers.pd.read_excel", return_value=dataframe):
        result: list[dict[str, Any]] = read_transactions_from_excel(
            "data/transactions_excel.xlsx"
        )

    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)


def test_read_transactions_from_csv_uses_pandas() -> None:
    """Тестирует вызов pandas.read_csv."""
    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = []

    with patch("src.file_handlers.pd.read_csv", return_value=mock_dataframe):
        read_transactions_from_csv("data/transactions.csv")

    mock_dataframe.to_dict.assert_called_once_with(orient="records")


def test_read_transactions_from_excel_uses_pandas() -> None:
    """Тестирует вызов pandas.read_excel."""
    mock_dataframe = Mock()
    mock_dataframe.to_dict.return_value = []

    with patch("src.file_handlers.pd.read_excel", return_value=mock_dataframe):
        read_transactions_from_excel("data/transactions_excel.xlsx")

    mock_dataframe.to_dict.assert_called_once_with(orient="records")
