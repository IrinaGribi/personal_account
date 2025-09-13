import pytest

from src.decorators import log


def test_successful_function_console_output(capsys):
    """Тест успешного выполнения функции с выводом в консоль"""

    @log()
    def add_numbers(a, b):
        return a + b

    result = add_numbers(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert captured.out == "add_numbers ok\n"


def test_function_with_exception_console(capsys):
    """Тест функции с исключением - вывод в консоль"""

    @log()
    def divide_numbers(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

    captured = capsys.readouterr()
    assert captured.out == "divide_numbers error: ZeroDivisionError. Inputs: (10, 0), {}\n"


def test_successful_function_file_output():
    """Тест успешного выполнения функции с записью в файл"""
    test_filename = "test_log.txt"

    @log(filename=test_filename)
    def multiply(x, y):
        return x * y

    result = multiply(4, 5)
    assert result == 20

    with open(test_filename, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == "multiply ok\n"


def test_function_with_exception_file_output():
    """Тест функции с исключением - запись в файл"""
    test_filename = "test_log.txt"

    @log(filename=test_filename)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open(test_filename, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n"
