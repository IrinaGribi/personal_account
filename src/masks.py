def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    card_number = card_number.replace(" ", "")
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    account_number = account_number.replace(" ", "")
    masked = f"**{account_number[-4:]}"
    return masked
