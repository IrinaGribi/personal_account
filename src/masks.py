import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
log_file_path = os.path.join(log_dir, "masks.log")

logger = logging.getLogger("masks")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    card_number = card_number.replace(" ", "")
    if len(card_number) != 16 or card_number == "":
        logger.error("Введен некорректный номер карты")
        raise ValueError("Номер карты должен содержать 16 цифр")
    if not card_number.isdigit():
        logger.error("Введен некорректный номер карты с символами")
        raise ValueError("Номер карты должен содержать только цифры")
    else:
        logger.info("Введен корректный номер карты, создана маска карты")
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    account_number = account_number.replace(" ", "")
    if len(account_number) != 20 or account_number == "":
        logger.error("Введен некорректный номер счета")
        raise ValueError("Номер счета должен содержать 20 цифр")
    if not account_number.isdigit():
        logger.error("Введен некорректный номер счета с символами")
        raise ValueError("Номер счета должен содержать только цифры")
    else:
        logger.info("Введен корректный номер счета, создана маска счета")
        masked = f"**{account_number[-4:]}"
        return masked


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
