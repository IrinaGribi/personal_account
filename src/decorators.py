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
                log_message = f"{func_name} ok"

                # Записываем лог в файл или консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                log_message = f"{func_name} error: {error_type}. Inputs: {args}, {kwargs}"

                # Записываем лог в файл или консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                # Перевызываем исключение
                raise

        return wrapper

    return decorator
