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
