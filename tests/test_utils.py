from typing import Any
from unittest.mock import mock_open, patch

from src.utils import load_transactions_from_json


def test_load_transactions_from_json_success() -> None:
    """Тестирует успешное чтение списка транзакций из JSON-файла."""
    json_data = '[{"id": 1, "state": "EXECUTED"}]'

    with patch("pathlib.Path.open", mock_open(read_data=json_data)):
        result = load_transactions_from_json("data/operations.json")

    assert result == [{"id": 1, "state": "EXECUTED"}]


def test_load_transactions_from_json_empty_file() -> None:
    """Тестирует чтение пустого JSON-файла."""
    with patch("pathlib.Path.open", mock_open(read_data="")):
        result = load_transactions_from_json("data/operations.json")

    assert result == []


def test_load_transactions_from_json_not_list() -> None:
    """Тестирует чтение JSON-файла, который содержит не список."""
    json_data = '{"id": 1, "state": "EXECUTED"}'

    with patch("pathlib.Path.open", mock_open(read_data=json_data)):
        result = load_transactions_from_json("data/operations.json")

    assert result == []


def test_load_transactions_from_json_file_not_found() -> None:
    """Тестирует чтение несуществующего JSON-файла."""
    with patch("pathlib.Path.open", side_effect=FileNotFoundError):
        result = load_transactions_from_json("data/operations.json")

    assert result == []


def test_load_transactions_from_json_returns_list_of_dicts() -> None:
    """Тестирует тип возвращаемого значения при корректном JSON-файле."""
    json_data = '[{"id": 1}, {"id": 2}]'

    with patch("pathlib.Path.open", mock_open(read_data=json_data)):
        result = load_transactions_from_json("data/operations.json")

    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)


def test_load_transactions_from_json_type_hint() -> None:
    """Проверяет, что результат можно использовать как список словарей."""
    json_data = '[{"amount": "100.00"}]'

    with patch("pathlib.Path.open", mock_open(read_data=json_data)):
        result: list[dict[str, Any]] = load_transactions_from_json(
            "data/operations.json"
        )

    assert result[0]["amount"] == "100.00"
