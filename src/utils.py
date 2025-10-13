import json
import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
log_file_path = os.path.join(log_dir, "utils.log")

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_financial_transactions(file_path):
    """
    Читает JSON-файл с финансовыми транзакциями и возвращает список словарей
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.error(f"Файл {file_path} не найден")
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            logger.error(f"Файл {file_path} пустой")
            return []

        # Читаем и парсим JSON
        with open(file_path, "r", encoding="utf-8") as file:
            logger.info("Читаем и парсим JSON")
            data = json.load(file)

        # Проверяем, что данные представляют собой список
        if not isinstance(data, list):
            logger.error(f"Содержимое файла {file_path} не является списком")
            return []

        logger.info("Успешно загружено {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при парсинге JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []


if __name__ == "__main__":
    file_path = "../data/example.json"
    print(load_financial_transactions(file_path))
