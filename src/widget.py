from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Маскирует информацию о карте или счете."""
    last_space_index = card_info.rfind(" ")
    card_type = card_info[:last_space_index]
    number = card_info[last_space_index + 1:]

    if card_type.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """Возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    if len(date_string) < 10:
        raise ValueError("Дата не может быть пустой")
    else:
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
