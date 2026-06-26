"""Модуль с функциями для вычисления площади круга и форматирования описания."""

import math


def circle_area(radius: float) -> float:
    """
    Вычисляет площадь круга по радиусу.

    Args:
        radius: Радиус круга.

    Returns:
        Площадь круга.

    Example:
        >>> circle_area(5.0)
        78.53981633974483
    """
    return math.pi * radius * radius


def format_description(radius: float, area: float) -> str:
    """
    Форматирует строку с информацией о радиусе и площади.

    Args:
        radius: Радиус круга.
        area: Площадь круга.

    Returns:
        Отформатированная строка.

    Example:
        >>> format_description(5.0, 78.5398)
        'Radius is 5.0; area is 78.54'
    """
    return f"Radius is {radius}; area is {round(area, 2)}"


def get_info(radius: float) -> None:
    """
    Вычисляет площадь круга и выводит описание на экран.

    Args:
        radius: Радиус круга.
    """
    area = circle_area(radius)
    description = format_description(radius, area)
    print(description)