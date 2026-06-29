from typing import Any
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_transaction_amount_to_rub


@pytest.fixture
def rub_transaction() -> dict[str, Any]:
    """Возвращает транзакцию в рублях."""
    return {
        "operationAmount": {
            "amount": "1000.00",
            "currency": {
                "name": "руб.",
                "code": "RUB",
            },
        },
    }


@pytest.fixture
def usd_transaction() -> dict[str, Any]:
    """Возвращает транзакцию в долларах."""
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "name": "USD",
                "code": "USD",
            },
        },
    }


@pytest.fixture
def eur_transaction() -> dict[str, Any]:
    """Возвращает транзакцию в евро."""
    return {
        "operationAmount": {
            "amount": "50.00",
            "currency": {
                "name": "EUR",
                "code": "EUR",
            },
        },
    }


def test_convert_transaction_amount_to_rub_from_rub(
    rub_transaction: dict[str, Any],
) -> None:
    """Тестирует возврат суммы без конвертации для рублевой транзакции."""
    result = convert_transaction_amount_to_rub(rub_transaction)

    assert result == 1000.00


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_convert_transaction_amount_to_rub_from_usd(
    mock_getenv: Mock,
    mock_get: Mock,
    usd_transaction: dict[str, Any],
) -> None:
    """Тестирует конвертацию суммы из долларов в рубли."""
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000.00}
    mock_get.return_value = mock_response

    result = convert_transaction_amount_to_rub(usd_transaction)

    assert result == 9000.00
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_convert_transaction_amount_to_rub_from_eur(
    mock_getenv: Mock,
    mock_get: Mock,
    eur_transaction: dict[str, Any],
) -> None:
    """Тестирует конвертацию суммы из евро в рубли."""
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {"result": 5000.00}
    mock_get.return_value = mock_response

    result = convert_transaction_amount_to_rub(eur_transaction)

    assert result == 5000.00
    mock_get.assert_called_once()


@patch("src.external_api.os.getenv")
def test_convert_transaction_amount_to_rub_without_api_key(
    mock_getenv: Mock,
    usd_transaction: dict[str, Any],
) -> None:
    """Тестирует ошибку при отсутствии API-ключа."""
    mock_getenv.return_value = None

    with pytest.raises(ValueError):
        convert_transaction_amount_to_rub(usd_transaction)


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_convert_transaction_amount_to_rub_api_params(
    mock_getenv: Mock,
    mock_get: Mock,
    usd_transaction: dict[str, Any],
) -> None:
    """Тестирует параметры запроса к API конвертации валют."""
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000.00}
    mock_get.return_value = mock_response

    convert_transaction_amount_to_rub(usd_transaction)

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key"},
        params={
            "from": "USD",
            "to": "RUB",
            "amount": 100.00,
        },
    )


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_convert_transaction_amount_to_rub_calls_raise_for_status(
    mock_getenv: Mock,
    mock_get: Mock,
    usd_transaction: dict[str, Any],
) -> None:
    """Тестирует вызов проверки статуса ответа API."""
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000.00}
    mock_get.return_value = mock_response

    convert_transaction_amount_to_rub(usd_transaction)

    mock_response.raise_for_status.assert_called_once()
