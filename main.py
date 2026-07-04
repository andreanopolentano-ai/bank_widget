from typing import Any

from src.file_handlers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.processing import sort_by_date
from src.search import process_bank_search
from src.utils import load_transactions_from_json
from src.widget import get_date, mask_account_card


def main() -> None:
    """Запускает основную логику работы с банковскими транзакциями."""
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input()

    transactions = _load_transactions(file_choice)

    status = _get_valid_status()
    transactions = _filter_by_status(transactions, status)

    if _ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        reverse = _ask_sort_order()
        transactions = sort_by_date(transactions, reverse=reverse)

    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        transactions = _filter_rub_transactions(transactions)

    if _ask_yes_no(
        "Отфильтровать список транзакций по определенному слову "
        "в описании? Да/Нет"
    ):
        search = input("Введите слово для поиска в описании: ")
        transactions = process_bank_search(transactions, search)

    print("Распечатываю итоговый список транзакций...")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}")

    for transaction in transactions:
        print()
        print(_format_transaction(transaction))


def _load_transactions(file_choice: str) -> list[dict[str, Any]]:
    """Загружает транзакции из выбранного пользователем файла."""
    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        return load_transactions_from_json("data/operations.json")

    if file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        return read_transactions_from_csv("data/transactions.csv")

    if file_choice == "3":
        print("Для обработки выбран XLSX-файл.")
        return read_transactions_from_excel("data/transactions_excel.xlsx")

    print("Неверный пункт меню.")
    return []


def _get_valid_status() -> str:
    """Запрашивает у пользователя корректный статус операции."""
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        status = input().upper()

        if status in available_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status

        print(f'Статус операции "{status}" недоступен.')


def _filter_by_status(
    transactions: list[dict[str, Any]],
    status: str,
) -> list[dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    return [
        transaction
        for transaction in transactions
        if str(transaction.get("state", "")).upper() == status
    ]


def _ask_yes_no(question: str) -> bool:
    """Возвращает True, если пользователь ответил да."""
    answer = input(f"{question}\n").lower()

    return answer in ("да", "yes", "y")


def _ask_sort_order() -> bool:
    """Возвращает порядок сортировки по дате."""
    answer = input("Отсортировать по возрастанию или по убыванию?\n").lower()

    return answer != "по возрастанию"


def _filter_rub_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Возвращает только рублевые транзакции."""
    return [
        transaction
        for transaction in transactions
        if _get_currency_code(transaction) == "RUB"
    ]


def _get_currency_code(transaction: dict[str, Any]) -> str:
    """Возвращает код валюты транзакции."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency", {})
        if isinstance(currency, dict):
            return str(currency.get("code", ""))

    return str(transaction.get("currency_code", ""))


def _get_currency_name(transaction: dict[str, Any]) -> str:
    """Возвращает название валюты транзакции."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency", {})
        if isinstance(currency, dict):
            return str(currency.get("name", ""))

    return str(transaction.get("currency_name", ""))


def _get_amount(transaction: dict[str, Any]) -> str:
    """Возвращает сумму транзакции."""
    operation_amount = transaction.get("operationAmount")

    if isinstance(operation_amount, dict):
        return str(operation_amount.get("amount", ""))

    return str(transaction.get("amount", ""))


def _format_transaction(transaction: dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода пользователю."""
    date = get_date(str(transaction.get("date", "")))
    description = str(transaction.get("description", ""))
    amount = _get_amount(transaction)
    currency_name = _get_currency_name(transaction)

    source = transaction.get("from")
    destination = transaction.get("to")

    if source and destination:
        transfer_line = (
            f"{mask_account_card(str(source))} -> "
            f"{mask_account_card(str(destination))}"
        )
    elif destination:
        transfer_line = mask_account_card(str(destination))
    else:
        transfer_line = ""

    return (
        f"{date} {description}\n"
        f"{transfer_line}\n"
        f"Сумма: {amount} {currency_name}"
    )


if __name__ == "__main__":
    main()
