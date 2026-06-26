"""Модуль с функциями маскировки номеров карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя первые 6 и последние 4 цифры.

    Формат вывода: XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты в виде строки (может содержать пробелы).

    Returns:
        Замаскированный номер карты.

    Example:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    # Убираем пробелы, если они есть
    number = card_number.replace(" ", "")
    # Формируем маску
    masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляя только последние 4 цифры.

    Формат вывода: **XXXX.

    Args:
        account_number: Номер счета в виде строки.

    Returns:
        Замаскированный номер счета.

    Example:
        >>> get_mask_account("73654108430135874305")
        '**4305'
    """
    # Показываем только последние 4 символа, перед ними две звездочки
    masked = f"**{account_number[-4:]}"
    return masked
