import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Тестирует маскировку номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("1234", "**1234"),
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    """Тестирует маскировку номера счета."""
    assert get_mask_account(account_number) == expected