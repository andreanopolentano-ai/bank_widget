from typing import Any
from unittest.mock import patch

from main import (
    _filter_by_status,
    _filter_rub_transactions,
    _format_transaction,
    _get_amount,
    _get_currency_code,
    _get_currency_name,
    _load_transactions,
    main,
)


def test_load_transactions_json() -> None:
    """Тестирует загрузку транзакций из JSON-файла."""
    with patch("main.load_transactions_from_json", return_value=[{"id": 1}]):
        result = _load_transactions("1")

    assert result == [{"id": 1}]


def test_load_transactions_csv() -> None:
    """Тестирует загрузку транзакций из CSV-файла."""
    with patch("main.read_transactions_from_csv", return_value=[{"id": 1}]):
        result = _load_transactions("2")

    assert result == [{"id": 1}]


def test_load_transactions_excel() -> None:
    """Тестирует загрузку транзакций из Excel-файла."""
    with patch("main.read_transactions_from_excel", return_value=[{"id": 1}]):
        result = _load_transactions("3")

    assert result == [{"id": 1}]


def test_load_transactions_wrong_choice() -> None:
    """Тестирует неверный выбор источника данных."""
    result = _load_transactions("wrong")

    assert result == []


def test_filter_by_status() -> None:
    """Тестирует фильтрацию транзакций по статусу."""
    transactions: list[dict[str, Any]] = [
        {"state": "EXECUTED"},
        {"state": "CANCELED"},
        {"state": "executed"},
    ]

    result = _filter_by_status(transactions, "EXECUTED")

    assert result == [
        {"state": "EXECUTED"},
        {"state": "executed"},
    ]


def test_filter_rub_transactions() -> None:
    """Тестирует фильтрацию рублевых транзакций."""
    transactions: list[dict[str, Any]] = [
        {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "руб.", "code": "RUB"},
            }
        },
        {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        },
    ]

    result = _filter_rub_transactions(transactions)

    assert result == [
        {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "руб.", "code": "RUB"},
            }
        }
    ]


def test_get_currency_code_from_operation_amount() -> None:
    """Тестирует получение кода валюты из operationAmount."""
    transaction = {
        "operationAmount": {
            "currency": {"code": "RUB"},
        }
    }

    result = _get_currency_code(transaction)

    assert result == "RUB"


def test_get_currency_code_from_csv_field() -> None:
    """Тестирует получение кода валюты из поля CSV/XLSX."""
    transaction = {
        "currency_code": "USD",
    }

    result = _get_currency_code(transaction)

    assert result == "USD"


def test_get_currency_name_from_operation_amount() -> None:
    """Тестирует получение названия валюты из operationAmount."""
    transaction = {
        "operationAmount": {
            "currency": {"name": "руб."},
        }
    }

    result = _get_currency_name(transaction)

    assert result == "руб."


def test_get_currency_name_from_csv_field() -> None:
    """Тестирует получение названия валюты из поля CSV/XLSX."""
    transaction = {
        "currency_name": "USD",
    }

    result = _get_currency_name(transaction)

    assert result == "USD"


def test_get_amount_from_operation_amount() -> None:
    """Тестирует получение суммы из operationAmount."""
    transaction = {
        "operationAmount": {
            "amount": "40542",
        }
    }

    result = _get_amount(transaction)

    assert result == "40542"


def test_get_amount_from_csv_field() -> None:
    """Тестирует получение суммы из поля CSV/XLSX."""
    transaction = {
        "amount": "130",
    }

    result = _get_amount(transaction)

    assert result == "130"


def test_format_transaction() -> None:
    """Тестирует форматирование транзакции для вывода."""
    transaction = {
        "date": "2019-12-08T22:46:21.935582",
        "description": "Открытие вклада",
        "to": "Счет 12345678901234564321",
        "operationAmount": {
            "amount": "40542",
            "currency": {"name": "руб.", "code": "RUB"},
        },
    }

    result = _format_transaction(transaction)

    assert "08.12.2019 Открытие вклада" in result
    assert "Счет **4321" in result
    assert "Сумма: 40542 руб." in result


@patch("main.load_transactions_from_json")
def test_main_empty_result(
    mock_load_json: Any,
    capsys: Any,
) -> None:
    """Тестирует вывод сообщения при пустой итоговой выборке."""
    mock_load_json.return_value = [
        {
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "description": "Открытие вклада",
            "to": "Счет 12345678901234564321",
            "operationAmount": {
                "amount": "40542",
                "currency": {"name": "руб.", "code": "RUB"},
            },
        }
    ]

    user_inputs = [
        "1",
        "CANCELED",
        "нет",
        "нет",
        "нет",
    ]

    with patch("builtins.input", side_effect=user_inputs):
        main()

    captured = capsys.readouterr()

    assert "Не найдено ни одной транзакции" in captured.out


@patch("main.load_transactions_from_json")
def test_main_success(
    mock_load_json: Any,
    capsys: Any,
) -> None:
    """Тестирует успешный сценарий работы main."""
    mock_load_json.return_value = [
        {
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "description": "Открытие вклада",
            "to": "Счет 12345678901234564321",
            "operationAmount": {
                "amount": "40542",
                "currency": {"name": "руб.", "code": "RUB"},
            },
        }
    ]

    user_inputs = [
        "1",
        "executed",
        "нет",
        "да",
        "нет",
    ]

    with patch("builtins.input", side_effect=user_inputs):
        main()

    captured = capsys.readouterr()

    assert "Всего банковских операций в выборке: 1" in captured.out
    assert "Открытие вклада" in captured.out
