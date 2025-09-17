import json
import os


def load_financial_transactions(file_path):
    """
    Читает JSON-файл с финансовыми транзакциями и возвращает список словарей
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден")
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            print(f"Файл {file_path} пустой")
            return []

        # Читаем и парсим JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные представляют собой список
        if not isinstance(data, list):
            print(f"Содержимое файла {file_path} не является списком")
            return []

        print(f"Успешно загружено {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
