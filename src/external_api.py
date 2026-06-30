import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


def convert_transaction_amount_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR"):
        return _convert_currency_to_rub(amount, currency_code)

    return amount


def _convert_currency_to_rub(amount: float, currency_code: str) -> float:
    """Конвертирует сумму из USD или EUR в рубли через внешний API."""
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")

    if api_key is None:
        raise ValueError("EXCHANGE_RATES_API_KEY is not set")

    url = "https://api.apilayer.com/exchangerates_data/convert"

    params = {
        "from": currency_code,
        "to": "RUB",
        "amount": amount,
    }

    headers = {
        "apikey": api_key,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    return float(data["result"])
