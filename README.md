# Bank Widget

Проект содержит функции для обработки данных о банковских операциях клиента.

## Реализованные функции

### `filter_by_state`

Функция принимает список словарей с банковскими операциями и значение статуса операции.

По умолчанию функция возвращает операции со статусом `EXECUTED`.

Пример использования:

```python
from src.processing import filter_by_state

operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

print(filter_by_state(operations))
print(filter_by_state(operations, "CANCELED"))
```

### `sort_by_date`

Функция принимает список словарей с банковскими операциями и сортирует его по дате.

По умолчанию сортировка выполняется по убыванию, то есть сначала идут самые новые операции.

Пример использования:

```python
from src.processing import sort_by_date

operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
]

print(sort_by_date(operations))
print(sort_by_date(operations, False))
```

## Установка проекта

Клонируйте репозиторий:

```bash
git clone https://github.com/andreanopolentano-ai/bank_widget.git
```

Перейдите в папку проекта:

```bash
cd bank_widget
```

Установите зависимости:

```bash
poetry install
```

## Тестирование

Для запуска тестов используйте команду:

```bash
poetry run pytest
```

Для формирования HTML-отчёта покрытия тестами используйте команду:

```bash
poetry run pytest --cov=src --cov-report=html
```

После выполнения команды HTML-отчёт будет доступен в папке:

```text
htmlcov/index.html
```

## Проверка покрытия

Для просмотра покрытия в терминале используйте команду:

```bash
poetry run pytest --cov=src
```

Функциональный код должен быть покрыт тестами более чем на 80%.
