from unittest.mock import mock_open, patch

import pandas as pd

from src.file_reader import read_transactions_csv, read_transactions_excel


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="date;amount;description\n2024-01-01;1000;Зарплата\n2024-01-02;-500;Продукты")
@patch("csv.DictReader")
def test_read_transactions_csv_success(mock_dict_reader, mock_file, example_transactions_list):
    '''Успешное чтение CSV-файла'''
    # Подменяю возвращаемое значение DictReader
    mock_dict_reader.return_value = example_transactions_list

    result = read_transactions_csv("transactions.csv")

    assert result == example_transactions_list
    assert len(result) == 2
    assert result[0]["date"] == "2024-01-01"
    assert result[1]["description"] == "Продукты"

    # Проверяю, что open был вызван правильно
    mock_file.assert_called_once_with("transactions.csv", encoding="utf-8")


@patch("pandas.read_excel")
def test_read_transactions_excel_success(mock_read_excel):
    '''Успешное чтение Excel-файла'''
    # Создаю поддельный DataFrame
    mock_df = pd.DataFrame([
        {"date": "2024-01-01", "amount": 1000, "description": "Зарплата"},
        {"date": "2024-01-02", "amount": -500, "description": "Продукты"}
    ])
    mock_read_excel.return_value = mock_df

    result = read_transactions_excel("transactions.xlsx")
    assert len(result) == 2
    assert result[0]["date"] == "2024-01-01"
    assert result[1]["description"] == "Продукты"

    # Проверяю вызов
    mock_read_excel.assert_called_once_with("transactions.xlsx")
