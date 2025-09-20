import json
from unittest.mock import mock_open, patch

from src.utils import load_financial_transactions


@patch("os.path.exists", return_value=False)
def test_file_not_found(mock_exists):
    '''Файл не существует'''
    result = load_financial_transactions("fake_file.json")
    assert result == []
    mock_exists.assert_called_once_with("fake_file.json")


@patch("os.path.exists", return_value=True)
@patch("os.path.getsize", return_value=0)
def test_file_empty(mock_getsize, mock_exists):
    '''Файл существует, но пустой'''
    result = load_financial_transactions("empty_file.json")
    assert result == []
    mock_exists.assert_called_once()
    mock_getsize.assert_called_once_with("empty_file.json")


@patch("os.path.exists", return_value=True)
@patch("os.path.getsize", return_value=100)
@patch("builtins.open", new_callable=mock_open)
def test_success_load(mock_file, mock_getsize, mock_exists, example_transactions):
    '''Успешная загрузка списка транзакций'''
    mock_file.return_value.read.return_value = json.dumps(example_transactions)
    result = load_financial_transactions("transactions.json")
    assert result == example_transactions
    assert len(result) == 5


@patch("os.path.exists", return_value=True)
@patch("os.path.getsize", return_value=50)
@patch("builtins.open", new_callable=mock_open)
def test_json_not_a_list(mock_file, mock_getsize, mock_exists):
    '''Содержимое файла — не список, а словарь'''
    mock_file.return_value.read.return_value = json.dumps({"error": "not a list"})
    result = load_financial_transactions("not_list.json")
    assert result == []
    mock_file.assert_called_once_with("not_list.json", "r", encoding="utf-8")
