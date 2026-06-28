import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_card, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(account_card: str, expected: str) -> None:
    """Тестирует маскировку карты или счета."""
    assert mask_account_card(account_card) == expected


@pytest.mark.parametrize(
    "incorrect_value",
    [
        "",
        "Visa",
        "Visa Platinum abcdef",
    ],
)
def test_mask_account_card_incorrect_value(incorrect_value: str) -> None:
    """Тестирует обработку некорректных входных данных."""
    assert mask_account_card(incorrect_value) == "Некорректный ввод"


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ],
)
def test_get_date(date_string: str, expected: str) -> None:
    """Тестирует преобразование даты в формат ДД.ММ.ГГГГ."""
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "incorrect_date",
    [
        "",
        "2024-03-11",
        "incorrect date",
    ],
)
def test_get_date_incorrect_value(incorrect_date: str) -> None:
    """Тестирует обработку некорректной даты."""
    with pytest.raises(ValueError):
        get_date(incorrect_date)
