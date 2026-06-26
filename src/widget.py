"""Модуль для обработки информации о картах и счетах."""

from datetime import datetime
from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счета в строке типа 'Visa Platinum 7000792289606361'.

    Различает карты и счета по наличию слова 'Счет' в начале строки.
    Для карт применяет формат XXXX XX** **** XXXX, для счетов — **XXXX.
    Если строка не соответствует формату, возвращает сообщение об ошибке.

    Args:
        info: Строка с типом и номером карты или счета.

    Returns:
        Строка с замаскированным номером.

    Examples:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    # Защита от некорректного ввода
    if not info or " " not in info:
        return "Некорректный ввод"

    # Разделяем по последнему пробелу: тип и номер
    parts = info.rsplit(" ", 1)
    if len(parts) != 2:
        return "Некорректный ввод"

    type_part, number_part = parts

    # Проверяем, что номер состоит только из цифр (после удаления возможных пробелов)
    clean_number = number_part.replace(" ", "")
    if not clean_number.isdigit():
        return "Некорректный ввод"

    # Определяем, счет это или карта, и применяем нужную маскировку
    if type_part.startswith("Счет"):
        masked_number = get_mask_account(clean_number)
    else:
        masked_number = get_mask_card_number(clean_number)

    return f"{type_part} {masked_number}"


def get_date(iso_date: str) -> str:
    """
    Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ.

    Args:
        iso_date: Строка с датой в формате 'YYYY-MM-DDTHH:MM:SS.ffffff'.

    Returns:
        Дата в виде 'DD.MM.YYYY'.

    Example:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    # Парсим строку в объект datetime
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%f")
    # Возвращаем отформатированную дату
    return dt.strftime("%d.%m.%Y")
