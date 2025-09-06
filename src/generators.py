def filter_by_currency(transactions, currency_code):
    """
    Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной
    """
    result = (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code
    )
    return result


def transaction_descriptions(transactions):
    """
    Принимает список словарей с транзакциями и
    возвращает описание каждой операции по очереди
    """
    for transaction in transactions:
        description = transaction.get("description", "Описание отсутствует")
        yield description


def card_number_generator(start, end):
    """
    Выдает номера банковских карт в формате XXXX XXXX XXXX XXXX
    """
    if start < 1 or end > 9999999999999999:
        raise ValueError("Диапазон должен быть от 1 до 9999999999999999")

    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    for number in range(start, end + 1):
        card_number = f"{number:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"

