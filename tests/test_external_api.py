from unittest.mock import Mock, patch

import pytest

from src.external_api import get_transaction_amount_in_rubles


def test_get_transaction_amount_in_rubles_rub(example_transactions):
    """Если валюта RUB — возвращаем сумму как есть"""
    rub_transaction = example_transactions[2]
    result = get_transaction_amount_in_rubles(rub_transaction)
    assert result == 43318.34


@patch("src.external_api.requests.get")
def test_get_transaction_amount_in_rubles_usd(mock_get, example_transactions):
    """Если валюта USD — делаем запрос к API"""
    usd_transaction = example_transactions[0]

    # Создаем "поддельный" ответ от API
    mock_response = Mock()
    mock_response.json.return_value = {"result": 900000.0}
    mock_get.return_value = mock_response

    result = get_transaction_amount_in_rubles(usd_transaction)
    assert result == 900000.0


def test_get_transaction_amount_in_rubles_no_currency(example_transactions):
    """Если валюта не указана — возвращаем 0.0"""
    broken_transaction = {
        "operationAmount": {
            "amount": "100",
        }
    }

    result = get_transaction_amount_in_rubles(broken_transaction)
    assert result == 0.0
