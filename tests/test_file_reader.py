from unittest.mock import mock_open, patch

import pandas as pd

from src.file_reader import read_transactions_csv, read_transactions_excel


def test_read_transactions_csv_success():
    """
    Успешное чтение CSV-файла: проверяет, что данные правильно преобразуются
    из плоской CSV-структуры во вложенный формат транзакций.
    """
    # Подготавливаем CSV-данные, как они выглядят в файле
    csv_content = (
        "date;amount;description\n"
        "2024-01-01;1000;Зарплата\n"
        "2024-01-02;-500;Продукты"
    )

    # Мокаем открытие файла
    with patch("builtins.open", mock_open(read_data=csv_content)):
        result = read_transactions_csv("transactions.csv")

    # Ожидаемый результат после обработки функцией
    expected = [
        {
            "id": "",
            "state": "",
            "date": "2024-01-01",
            "description": "Зарплата",
            "from": "",
            "to": "",
            "operationAmount": {
                "amount": "1000",
                "currency": {"name": "", "code": "RUB"}
            }
        },
        {
            "id": "",
            "state": "",
            "date": "2024-01-02",
            "description": "Продукты",
            "from": "",
            "to": "",
            "operationAmount": {
                "amount": "-500",
                "currency": {"name": "", "code": "RUB"}
            }
        }
    ]

    # Проверки
    assert result == expected
    assert len(result) == 2
    assert result[0]["date"] == "2024-01-01"
    assert result[1]["description"] == "Продукты"


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
