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


def test_successful_function_file_output(temp_log_file):
    """Тест успешного выполнения функции с записью в файл"""

    @log(filename=str(temp_log_file))  # Использую создание временного файла через фикстуру
    def multiply(x, y):
        return x * y

    result = multiply(4, 5)
    assert result == 20

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == "multiply ok\n"


def test_function_with_exception_file_output(temp_log_file):
    """Тест функции с исключением - запись в файл"""

    @log(filename=str(temp_log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n"
