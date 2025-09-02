def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    card_number = card_number.replace(" ", "")
    if len(card_number) != 16 or card_number == "":
        raise ValueError("Номер карты должен содержать 16 цифр")
    if not card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    else:
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    account_number = account_number.replace(" ", "")
    if len(account_number) != 20 or account_number == "":
        raise ValueError("Номер счета должен содержать 20 цифр")
    if not account_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    else:
        masked = f"**{account_number[-4:]}"
        return masked


