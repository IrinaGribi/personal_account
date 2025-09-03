import pytest

from src.widget import get_date, mask_account_card


def test_account_masking() -> str:
    """Тест маскировки счета"""
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"


def test_card_masking() -> str:
    """Тест маскировки карты"""
    assert mask_account_card("Visa Classic 4111111111111111") == "Visa Classic 4111 11** **** 1111"


def test_case_insensitive_account() -> str:
    """Тест что слово 'счет' работает в разных регистрах"""
    assert mask_account_card("СЧЕТ 41111111111111112856") == "СЧЕТ **2856"


@pytest.mark.parametrize(
    "card_info, expected",
    [
        ("Visa Classic 4111111111111111", "Visa Classic 4111 11** **** 1111"),
        ("MasterCard Gold 5555555555554444", "MasterCard Gold 5555 55** **** 4444"),
        ("Maestro 6759649826438453", "Maestro 6759 64** **** 8453"),
        ("Счет 12345678901234563456", "Счет **3456"),
    ],
)
def test_card_types(card_info, expected) -> None:
    """Параметризованный тест что типы карт сохраняются"""
    assert mask_account_card(card_info) == expected


def test_basic_date_conversion() -> str:
    """Тест основного преобразования даты"""
    assert get_date("2023-03-11T02:26:18.671407") == "11.03.2023"


def test_empty_string() -> None:
    """Тест пустой строки"""
    with pytest.raises(ValueError):
        get_date("")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2023-03-11T02:26:18.671407", "11.03.2023"),
        ("2021-12-25T00:00:00", "25.12.2021"),
        ("2022-01-01T23:59:59", "01.01.2022"),
        ("2020-02-29T12:30:45", "29.02.2020"),
    ],
)
def test_date_parts(value: str, expected: str):
    """Параметризованный тест для проверки частей даты"""
    assert get_date(value) == expected
