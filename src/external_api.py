import os

import requests
from dotenv import load_dotenv

load_dotenv("../.env")

API_KEY = os.getenv("API_KEY")


def get_transaction_amount_in_rubles(transaction):
    """Принимает транзакцию и возвращает сумму в рублях"""
    # Получаем сумму транзакции
    amount = transaction.get("operationAmount", {}).get("amount", 0)

    # Получаем валюту транзакции
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    # Если валюта не определена — возвращаем 0.0
    if not currency_code:
        return 0.0

    # Если валюта уже рубли, возвращаем как есть
    if currency_code == "RUB":
        return float(amount)

    url = "https://api.apilayer.com/exchangerates_data/convert"

    payload = {"from": currency_code, "to": "RUB", "amount": amount}
    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers, params=payload)
    float_response = float(response.json()["result"])

    return float_response
