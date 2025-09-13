import functools


def log(filename=None):
    """
    Декоратор для логирования выполнения функций
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успешном выполнении
                log_message = f"{func_name} ok\n"

                # Записываем лог
                _write_log(log_message, filename)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                log_message = f"{func_name} error: {error_type}. Inputs: {args}, {kwargs}\n"

                # Записываем лог
                _write_log(log_message, filename)

                # Перевызываем исключение
                raise

        return wrapper

    return decorator


def _write_log(message, filename):
    """
    Вспомогательная функция для записи лога в файл или консоль
    """
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message.rstrip())