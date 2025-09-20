import csv

import pandas as pd


def read_transactions_csv(file_path):
    '''
    Считывает финансовые операции из CSV и выдает список словарей с транзакциями
    '''
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        dictionary_list = []
        for row in reader:
            dictionary_list.append(row)
        return dictionary_list


def read_transactions_excel(file_path):
    '''
    Считывает финансовые операции из EXCEL и выдает список словарей с транзакциями
    '''
    df = pd.read_excel(file_path)
    transactions = df.to_dict(orient="records")
    return transactions


if __name__ == "__main__":
    file_path = "../data/transactions.csv"
    file_path_2 = "../data/transactions_excel.xlsx"
    print(read_transactions_csv(file_path))
    print(read_transactions_excel(file_path_2))
