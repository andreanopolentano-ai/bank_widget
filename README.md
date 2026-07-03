# Bank Widget

Проект содержит функции для обработки банковских данных, маскировки номеров карт и счетов, фильтрации операций, генерации данных по транзакциям и логирования выполнения функций.

## Установка

Для установки зависимостей используется Poetry.

```bash
poetry install
```

## Запуск тестов

Для запуска всех тестов:

```bash
poetry run pytest
```

Для запуска тестов с отчетом покрытия:

```bash
poetry run pytest --cov=src --cov-report=html
```

HTML-отчет покрытия формируется в папке `htmlcov`.

## Проверка кода

Для проверки кода линтером Flake8:

```bash
poetry run flake8 src tests
```

## Модуль `masks`

Модуль `masks` содержит функции для маскировки номеров банковских карт и счетов.

### `get_mask_card_number`

Функция принимает номер карты и возвращает его в замаскированном виде.

Пример:

```python
from src.masks import get_mask_card_number

print(get_mask_card_number("7000792289606361"))
```

Результат:

```text
7000 79** **** 6361
```

### `get_mask_account`

Функция принимает номер счета и возвращает его в замаскированном виде.

Пример:

```python
from src.masks import get_mask_account

print(get_mask_account("73654108430135874305"))
```

Результат:

```text
**4305
```

## Модуль `widget`

Модуль `widget` содержит функции для подготовки данных к отображению пользователю.

### `mask_account_card`

Функция принимает строку с типом и номером карты или счета и возвращает строку с замаскированным номером.

Пример:

```python
from src.widget import mask_account_card

print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))
```

Результат:

```text
Visa Platinum 7000 79** **** 6361
Счет **4305
```

### `get_date`

Функция принимает дату в формате ISO и возвращает дату в формате `ДД.ММ.ГГГГ`.

Пример:

```python
from src.widget import get_date

print(get_date("2024-03-11T02:26:18.671407"))
```

Результат:

```text
11.03.2024
```

## Модуль `processing`

Модуль `processing` содержит функции для фильтрации и сортировки банковских операций.

### `filter_by_state`

Функция принимает список операций и возвращает только операции с указанным статусом.

Пример:

```python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
    {"id": 2, "state": "CANCELED", "date": "2024-01-02T10:00:00"},
]

print(filter_by_state(operations))
```

Результат:

```text
[{'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T10:00:00'}]
```

### `sort_by_date`

Функция принимает список операций и возвращает список, отсортированный по дате.

Пример:

```python
from src.processing import sort_by_date

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
    {"id": 2, "state": "EXECUTED", "date": "2024-01-02T10:00:00"},
]

print(sort_by_date(operations))
```

Результат:

```text
[
    {'id': 2, 'state': 'EXECUTED', 'date': '2024-01-02T10:00:00'},
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T10:00:00'}
]
```

## Модуль `generators`

Модуль `generators` содержит функции для работы с большими объемами данных транзакций через итераторы и генераторы.

### `filter_by_currency`

Функция принимает список транзакций и код валюты. Возвращает итератор, который по очереди выдает только транзакции с указанной валютой.

Пример:

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")

for transaction in usd_transactions:
    print(transaction)
```

### `transaction_descriptions`

Функция-генератор принимает список транзакций и по очереди возвращает описание каждой операции.

Пример:

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)

for description in descriptions:
    print(description)
```

### `card_number_generator`

Генератор принимает начальное и конечное значение диапазона и выдает номера банковских карт в формате `XXXX XXXX XXXX XXXX`.

Пример:

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

Результат:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

## Модуль `decorators`

Модуль `decorators` содержит декоратор `log`, который логирует выполнение функций.

### `log`

Декоратор `log` может выводить информацию о работе функции в консоль или записывать ее в файл.

Если аргумент `filename` не передан, лог выводится в консоль.

Пример:

```python
from src.decorators import log


@log()
def add_numbers(x, y):
    return x + y


add_numbers(1, 2)
```

Результат в консоли:

```text
add_numbers ok
```

Если передать `filename`, лог будет записан в файл.

Пример:

```python
from src.decorators import log


@log(filename="mylog.txt")
def add_numbers(x, y):
    return x + y


add_numbers(1, 2)
```

Результат в файле `mylog.txt`:

```text
add_numbers ok
```

Если функция завершится ошибкой, декоратор запишет имя функции, тип ошибки и входные параметры.

Пример:

```python
from src.decorators import log


@log()
def divide_numbers(x, y):
    return x / y


divide_numbers(1, 0)
```

Результат:

```text
divide_numbers error: ZeroDivisionError. Inputs: (1, 0), {}
```

## Тестирование

В проекте используются тесты на `pytest`.

Покрытие тестами проверяется командой:

```bash
poetry run pytest --cov=src
```

HTML-отчет покрытия создается командой:

```bash
poetry run pytest --cov=src --cov-report=html
```

Отчет находится в папке:

```text
htmlcov
```

## Модуль `utils`

Модуль `utils` содержит функцию для чтения данных о транзакциях из JSON-файла.

### `load_transactions_from_json`

Функция принимает путь к JSON-файлу и возвращает список словарей с данными о финансовых транзакциях.

Если файл не найден, пустой или содержит не список, функция возвращает пустой список.

Пример:

```python
from src.utils import load_transactions_from_json

transactions = load_transactions_from_json("data/operations.json")
print(transactions)

## Логирование

В проекте настроено логирование для модулей `masks` и `utils`.

Логи записываются в папку `logs` в корне проекта.

Файлы логов:

```text
logs/masks.log
logs/utils.log

## Модуль `file_handlers`

Модуль `file_handlers` содержит функции для чтения финансовых операций из CSV- и Excel-файлов.

### `read_transactions_from_csv`

Функция принимает путь к CSV-файлу и возвращает список словарей с транзакциями.

Пример:

```python
from src.file_handlers import read_transactions_from_csv

transactions = read_transactions_from_csv("data/transactions.csv")
print(transactions)

## Поиск и подсчет операций

В проекте добавлен модуль `search`.

### `process_bank_search`

Функция принимает список банковских операций и строку поиска. Возвращает список операций, у которых в поле `description` есть указанная строка.

Для поиска используется библиотека `re`.

Пример:

```python
from src.search import process_bank_search

result = process_bank_search(transactions, "Перевод")
print(result)
```

### `process_bank_operations`

Функция принимает список банковских операций и список категорий. Возвращает словарь, где ключи — названия категорий, а значения — количество операций в каждой категории.

Для подсчета используется `Counter` из библиотеки `collections`.

Пример:

```python
from src.search import process_bank_operations

categories = ["Перевод организации", "Открытие вклада"]
result = process_bank_operations(transactions, categories)
print(result)
```

## Основная программа

В корне проекта добавлен модуль `main`.

Функция `main` связывает функциональность проекта и позволяет пользователю:

- выбрать источник данных: JSON, CSV или XLSX;
- отфильтровать операции по статусу;
- отсортировать операции по дате;
- оставить только рублевые транзакции;
- выполнить поиск по описанию операции;
- вывести итоговый список операций в консоль.

Запуск основной программы:

```bash
python main.py
```
