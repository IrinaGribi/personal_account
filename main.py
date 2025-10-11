import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.utils import load_financial_transactions
from src.file_reader import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, sort_by_date, process_bank_search
from src.external_api import get_transaction_amount_in_rubles
from src.widget import get_date, mask_account_card


def main():
    """
    Основная функция программы, реализующая интерактивное меню
    для работы с банковскими транзакциями.
    """
    print("Программа: Привет! Добро пожаловать в программу работы "
          "с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice in ("1", "2", "3"):
            break
        else:
            print("Программа: Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

    data_dir = Path("data")

    # Загрузка транзакций в зависимости от выбора
    if choice == "1":
        file_path = data_dir / "operations.json"
        print("Программа: Для обработки выбран JSON-файл.")
        try:
            transactions = load_financial_transactions(str(file_path))
        except Exception as e:
            print(f"Программа: Ошибка при загрузке JSON-файла: {e}")
            return

    elif choice == "2":
        file_path = data_dir / "transactions.csv"
        print("Программа: Для обработки выбран CSV-файл.")
        try:
            transactions = read_transactions_csv(str(file_path))
        except Exception as e:
            print(f"Программа: Ошибка при чтении CSV-файла: {e}")
            return

    elif choice == "3":
        file_path = data_dir / "transactions_excel.xlsx"
        print("Программа: Для обработки выбран XLSX-файл.")
        try:
            transactions = read_transactions_excel(str(file_path))
        except Exception as e:
            print(f"Программа: Ошибка при чтении XLSX-файла: {e}")
            return

    # Проверка, загружены ли транзакции
    if not transactions:
        print("Программа: Не удалось загрузить транзакции.")
        return

    # Фильтрация по статусу
    valid_states = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        user_state = input("Пользователь: ").strip()
        normalized_state = user_state.upper()

        if normalized_state in valid_states:
            print(f'Программа: Операции отфильтрованы по статусу "{normalized_state}"')
            break
        else:
            print(f'Программа: Статус операции "{user_state}" недоступен.')

    filtered_transactions = filter_by_state(transactions, normalized_state)

    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_choice in ("да", "д", "yes", "y"):
        order_choice = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = True  # по умолчанию — убывание
        if "возрастанию" in order_choice:
            reverse = False
        elif "убыванию" in order_choice:
            reverse = True
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

    # Только рублёвые транзакции
    ruble_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if ruble_choice in ("да", "д", "yes", "y"):
        ruble_transactions = []
        for tr in filtered_transactions:
            try:
                amount_rub = get_transaction_amount_in_rubles(tr)
                if amount_rub is not None:
                    tr = tr.copy()
                    tr["_amount_rub"] = amount_rub
                    ruble_transactions.append(tr)
            except Exception:
                continue
        filtered_transactions = ruble_transactions

    # Фильтрация по слову в описании
    desc_filter_choice = input(
        "Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: "
    ).strip().lower()
    if desc_filter_choice in ("да", "д", "yes", "y"):
        search_word = input("Программа: Введите слово для поиска в описании:\nПользователь: ").strip()
        if search_word:
            filtered_transactions = process_bank_search(filtered_transactions, search_word)

    # Вывод результата
    print("Программа: Распечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")

    for tr in filtered_transactions:
        # Дата
        date_str = tr.get("date", "")
        formatted_date = get_date(date_str) if date_str else "Н/Д"

        # Описание
        description = tr.get("description", "Без описания")

        # Откуда и куда
        from_info = tr.get("from", "")
        to_info = tr.get("to", "")

        masked_from = mask_account_card(from_info) if from_info else ""
        masked_to = mask_account_card(to_info) if to_info else ""

        # Сумма
        if "_amount_rub" in tr:
            amount_str = f"{tr['_amount_rub']:.0f} руб."
        else:
            operation_amount = tr.get("operationAmount", {})
            amount = operation_amount.get("amount", "Н/Д")
            currency = operation_amount.get("currency", {}).get("code", "???")
            amount_str = f"{amount} {currency}"

        # Печать операции
        print(f"{formatted_date} {description}")

        if masked_from and masked_to:
            print(f"{masked_from} -> {masked_to}")
        elif masked_to:
            print(f"-> {masked_to}")
        elif masked_from:
            print(f"{masked_from} -> ")

        print(f"Сумма: {amount_str}\n")


if __name__ == "__main__":
    main()