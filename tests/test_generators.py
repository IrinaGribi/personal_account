import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Тесты filter_by_currency
def test_filter_by_usd_currency(example_transactions):
    """Тест фильтрации по USD валюте"""
    usd_transactions = list(filter_by_currency(example_transactions, "USD")) # все транзакции USD
    assert len(usd_transactions) == 3


def test_filter_by_rub_currency(example_transactions):
    """Тест фильтрации по RUB валюте"""
    rub_transactions = list(filter_by_currency(example_transactions, "RUB")) # все транзакции RUB
    assert len(rub_transactions) == 2


def test_filter_by_nonexistent_currency(example_transactions):
    """Тест фильтрации по несуществующей валюте"""
    eur_transactions = list(filter_by_currency(example_transactions, "EUR"))
    assert len(eur_transactions) == 0
    assert eur_transactions == []


def test_filter_empty_list(example_transactions):
    """Тест фильтрации пустого списка транзакций"""
    empty_transactions = list(filter_by_currency([], "USD"))
    assert len(empty_transactions) == 0
    assert empty_transactions == []


def test_filter_malformed_transactions():
    """Тест обработки некорректно сформированных транзакций"""
    malformed_transactions = [
        {"id": 1, "description": "Test"}, # Транзакция без operationAmount
        {"id": 2, "operationAmount": {"amount": "100"}}, # Транзакция без currency
        {"id": 3, "operationAmount": {"currency": {"name": "USD"}}}, # Транзакция без code в currency
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}}, # Нормальная транзакция
    ]
    usd_transactions = list(filter_by_currency(malformed_transactions, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 4


def test_work_generator_1(example_transactions):
    """Тест работы генератора"""
    usd_generator = filter_by_currency(example_transactions, "USD")
    first_transaction = next(usd_generator)
    assert first_transaction["id"] == 939719570
    assert first_transaction["operationAmount"]["currency"]["code"] == "USD"
    second_transaction = next(usd_generator)
    assert second_transaction["id"] == 142264268
    third_transaction = next(usd_generator)
    assert third_transaction["id"] == 895315941
    with pytest.raises(StopIteration):
        next(usd_generator)


# Тесты transaction_descriptions
def test_correct_descriptions_all_transactions(example_transactions):
    """Тест корректных описаний для всех транзакций"""
    descriptions_list = list(transaction_descriptions(example_transactions))
    assert len(descriptions_list) == 5
    assert descriptions_list == [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]


def test_work_generator(example_transactions):
    """Тест генератора"""
    descriptions_gen = transaction_descriptions(example_transactions)
    assert next(descriptions_gen) == "Перевод организации"
    assert next(descriptions_gen) == "Перевод со счета на счет"
    assert next(descriptions_gen) == "Перевод со счета на счет"
    assert next(descriptions_gen) == "Перевод с карты на карту"
    assert next(descriptions_gen) == "Перевод организации"
    with pytest.raises(StopIteration):
        next(descriptions_gen)


def test_empty_transactions_list():
    """Тест работы с пустым списком транзакций"""
    descriptions_list = list(transaction_descriptions([]))
    assert len(descriptions_list) == 0
    assert descriptions_list == []


def test_single_transaction(example_transactions):
    """Тест работы с одной транзакцией"""
    descriptions_gen = transaction_descriptions([example_transactions[0]])
    descriptions_list = list(descriptions_gen)
    assert len(descriptions_list) == 1
    assert descriptions_list[0] == "Перевод организации"


# Тесты card_number_generator
def test_basic_range_generation():
    """Тест генерации базового диапазона номеров карт"""
    generator = card_number_generator(1, 5)
    card_numbers = list(generator)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]
    assert len(card_numbers) == 5
    assert card_numbers == expected


def test_single_card_generation():
    """Тест генерации одного номера карты"""
    generator = card_number_generator(42, 42)
    card_numbers = list(generator)
    assert len(card_numbers) == 1
    assert card_numbers[0] == "0000 0000 0000 0042"


def test_large_range_generation():
    """Тест генерации большого диапазона"""
    card_numbers = list(card_number_generator(1000, 1010))
    assert len(card_numbers) == 11
    assert card_numbers[0] == "0000 0000 0000 1000"
    assert card_numbers[-1] == "0000 0000 0000 1010"


def test_lazy_evaluation():
    """Тест работы генератора"""
    generator = card_number_generator(1, 1000000)
    first_card = next(generator)
    assert first_card == "0000 0000 0000 0001"
    second_card = next(generator)
    assert second_card == "0000 0000 0000 0002"
    third_card = next(generator)
    assert third_card == "0000 0000 0000 0003"