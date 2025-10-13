import re


def filter_by_state(data_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'"""
    if not data_list:
        raise ValueError("Пустой список")

    result = []
    for item in data_list:
        if item.get("state") == state:
            result.append(item)
    return result


def sort_by_date(data_list: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по дате"""
    result = []
    for item in data_list:
        result.append(item)
    result.sort(key=lambda x: x.get("date", ""), reverse=reverse)
    return result


def process_bank_search(data, search):
    """
    Фильтрует список банковских операций по заданной строке поиска.
    """
    escaped_search = re.escape(search)

    pattern = re.compile(escaped_search, re.IGNORECASE)

    result = []
    for operation in data:
        description = operation.get("description", "")
        if pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data, categories):
    """
    Подсчитывает количество банковских операций по заданным категориям
    """
    result = {category: 0 for category in categories}

    compiled_patterns = {category: re.compile(re.escape(category), re.IGNORECASE) for category in categories}

    for operation in data:
        description = operation.get("description", "")

        for category, pattern in compiled_patterns.items():
            if pattern.search(description):
                result[category] += 1

    return result
