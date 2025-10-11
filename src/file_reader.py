import csv

import pandas as pd


def read_transactions_csv(file_path):
    """
    Считывает финансовые операции из CSV и выдает список словарей с транзакциями
    в формате, совместимом с JSON-структурой.
    """
    transactions = []
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            # Преобразуем плоскую CSV-структуру во вложенную, как в JSON
            transaction = {
                "id": row.get("id", ""),
                "state": row.get("state", ""),
                "date": row.get("date", ""),
                "description": row.get("description", ""),
                "from": row.get("from", ""),
                "to": row.get("to", ""),
                "operationAmount": {
                    "amount": row.get("amount", "0"),
                    "currency": {"name": row.get("currency_name", ""), "code": row.get("currency_code", "RUB")},
                },
            }
            transactions.append(transaction)
    return transactions


def read_transactions_excel(file_path):
    """
    Считывает финансовые операции из EXCEL и выдает список словарей с транзакциями
    в формате, совместимом с JSON-структурой.
    """
    df = pd.read_excel(file_path)
    transactions = []
    for _, row in df.iterrows():
        transaction = {
            "id": str(row.get("id", "")),
            "state": str(row.get("state", "")),
            "date": str(row.get("date", "")),
            "description": str(row.get("description", "")),
            "from": str(row.get("from", "")),
            "to": str(row.get("to", "")),
            "operationAmount": {
                "amount": str(row.get("amount", "0")),
                "currency": {"name": str(row.get("currency_name", "")), "code": str(row.get("currency_code", "RUB"))},
            },
        }
        transactions.append(transaction)
    return transactions


if __name__ == "__main__":
    file_path = "../data/transactions.csv"
    file_path_2 = "../data/transactions_excel.xlsx"
    print(read_transactions_csv(file_path))
    print(read_transactions_excel(file_path_2))
