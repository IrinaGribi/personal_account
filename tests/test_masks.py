import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_standard_card_number_without_spaces() -> str:
    """Тестирование стандартного номера карты без пробелов"""
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"


def test_standard_card_number_with_spaces() -> str:
    """Тестирование стандартного номера карты с пробелами"""
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"


def test_short_card_number() -> str:
    """Тестирование короткого номера карты"""
    with pytest.raises(ValueError):
        get_mask_card_number("152369")


def test_long_card_number() -> str:
    """Тестирование длинного номера карты"""
    with pytest.raises(ValueError):
        get_mask_card_number("152369852126984563")


def test_empty_string() -> None:
    """Тестирование пустой строки"""
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_card_number_with_letters() -> None:
    """Тестирование номера карты с буквами"""
    with pytest.raises(ValueError):
        get_mask_card_number("1563advb665")


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("4111111111111111", "4111 11** **** 1111"),
        ("5555 5555 5555 4444", "5555 55** **** 4444"),
        ("3782 822463100051", "3782 82** **** 0051"),
        ("60111111 1111 1117", "6011 11** **** 1117"),
    ],
)
def test_various_card_types(card_number: str, expected: str):
    """Параметризованный тест маски карты"""
    assert get_mask_card_number(card_number) == expected


def test_standard_account_number() -> str:
    """Тестирование стандартного номера счета"""
    assert get_mask_account("12345678901234567890") == "**7890"


def test_account_number_with_spaces() -> str:
    """Тестирование номера счета с пробелами"""
    assert get_mask_account("1234 5678 9012 3456 3456") == "**3456"


def test_short_card_number() -> None:
    """Тестирование короткого номера cчета"""
    with pytest.raises(ValueError):
        get_mask_account("152369")


def test_long_card_number() -> None:
    """Тестирование длинного номера счета"""
    with pytest.raises(ValueError):
        get_mask_account("152369852126984563264467463")


def test_empty_string() -> None:
    """Тестирование пустой строки"""
    with pytest.raises(ValueError):
        get_mask_account("")


def test_card_number_with_letters() -> None:
    """Тестирование номера счета с буквами"""
    with pytest.raises(ValueError):
        get_mask_account("1563advb665")


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("41111111111111111111", "**1111"),
        ("5555 5555 5555 4444 4444", "**4444"),
        ("3782 8224631000510051", "**0051"),
        ("60111111 1111 11171117", "**1117"),
    ],
)
def test_various_card_types(card_number: str, expected: str):
    """Параметризованный тест маски счета"""
    assert get_mask_account(card_number) == expected
