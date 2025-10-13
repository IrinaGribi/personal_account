import pytest

from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations


@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        ]
    ],
)
def test_filter_by_state(data: list, expected: list):
    """Параметризованный тест фильтрации, возвращает executed."""
    assert filter_by_state(data) == expected


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "CANCELED",
            [
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        )
    ],
)
def test_filter_by_state_canceled(data: list, state: str, expected: list):
    """Параметризованный тест фильтрации по статусу CANCELED."""
    assert filter_by_state(data, state) == expected


def test_filter_empty_list() -> None:
    """Тест с пустым списком"""
    with pytest.raises(ValueError):
        filter_by_state([])


@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        ]
    ],
)
def test_sort_by_date_without_is_reverse(data: list, expected: list):
    """Параметризованный тест сортировки в порядке убывания"""
    assert sort_by_date(data) == expected


@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ]
    ],
)
def test_sort_by_date_is_reverse(data: list, expected: list):
    """Параметризованный тест сортировки в порядке возрастания"""
    assert sort_by_date(data, False) == expected


def test_search_finds_matching_description():
    """Проверяет, что функция находит операцию, если строка поиска есть в описании."""
    data = [
        {"description": "Покупка в магазине"},
        {"description": "Зарплата"},
        {"description": "Перевод другу"}
    ]
    result = process_bank_search(data, "магазин")
    expected = [{"description": "Покупка в магазине"}]
    assert result == expected


def test_search_returns_empty_list_when_no_match():
    """Проверяет, что функция возвращает пустой список, если совпадений нет."""
    data = [
        {"description": "Зарплата"},
        {"description": "Аренда"}
    ]
    result = process_bank_search(data, "продукты")
    assert result == []


def test_search_is_case_insensitive():
    """Проверяет, что поиск не зависит от регистра букв (например, 'ЗАРПЛАТА' находит 'зарплата')."""
    data = [
        {"description": "зарплата"},
        {"description": "Покупка"}
    ]
    result = process_bank_search(data, "ЗАРПЛАТА")
    expected = [{"description": "зарплата"}]
    assert result == expected


def test_search_works_with_special_characters():
    """Проверяет, что поиск корректно работает со специальными символами, такими как скобки."""
    data = [
        {"description": "Оплата за интернет (январь)"},
        {"description": "Подписка на Netflix"}
    ]
    result = process_bank_search(data, "(январь)")
    expected = [{"description": "Оплата за интернет (январь)"}]
    assert result == expected


def test_search_handles_empty_description():
    """Проверяет, что функция корректно обрабатывает операции с пустым описанием."""
    data = [
        {"description": ""},
        {"description": "Зарплата"}
    ]
    result = process_bank_search(data, "зарплата")
    expected = [{"description": "Зарплата"}]
    assert result == expected


def test_search_with_empty_input_list():
    """Проверяет, что функция возвращает пустой список, если входной список операций пуст."""
    result = process_bank_search([], "любой текст")
    assert result == []


def test_search_with_empty_search_string():
    """Проверяет поведение при пустой строке поиска."""
    data = [{"description": "Зарплата"}, {"description": "Покупка"}]
    result = process_bank_search(data, "")
    # Пустая строка содержится в любом описании → все операции попадут в результат
    assert result == data


def test_search_in_operation_without_description_key():
    """Проверяет, что операции без ключа 'description' не вызывают ошибку и не попадают в результат."""
    data = [
        {"amount": 1000},  # нет 'description'
        {"description": "Зарплата"}
    ]
    result = process_bank_search(data, "зарплата")
    expected = [{"description": "Зарплата"}]
    assert result == expected


def test_search_matches_substring():
    """Проверяет, что поиск находит подстроку (например, 'плат' находит 'зарплата')."""
    data = [{"description": "Зарплата"}]
    result = process_bank_search(data, "плат")
    assert result == data


def test_multiple_matches():
    """Проверяет, что находятся все совпадения."""
    data = [
        {"description": "Оплата за интернет"},
        {"description": "Подписка на стриминг"},
        {"description": "Оплата за телефон"}
    ]
    result = process_bank_search(data, "оплата")
    assert len(result) == 2
    assert result[0]["description"] == "Оплата за интернет"
    assert result[1]["description"] == "Оплата за телефон"


def test_counts_operations_by_categories():
    """Проверяет, что функция правильно считает количество операций по каждой категории."""
    data = [
        {"description": "Покупка в магазине"},
        {"description": "Зарплата"},
        {"description": "Оплата за интернет"},
        {"description": "Покупка продуктов"}
    ]
    categories = ["покупка", "зарплата", "интернет"]
    result = process_bank_operations(data, categories)
    expected = {"покупка": 2, "зарплата": 1, "интернет": 1}
    assert result == expected


def test_returns_zero_for_categories_with_no_matches():
    """Проверяет, что категории без совпадений получают значение 0."""
    data = [{"description": "Зарплата"}]
    categories = ["продукты", "транспорт", "зарплата"]
    result = process_bank_operations(data, categories)
    expected = {"продукты": 0, "транспорт": 0, "зарплата": 1}
    assert result == expected


def test_search_is_case_independent():
    """Проверяет, что поиск по категориям не зависит от регистра."""
    data = [{"description": "ЗАРПЛАТА"}, {"description": "покупка"}]
    categories = ["зарплата", "ПОКУПКА"]
    result = process_bank_operations(data, categories)
    expected = {"зарплата": 1, "ПОКУПКА": 1}
    assert result == expected


def test_handles_special_characters_in_categories():
    """Проверяет, что категории со специальными символами (например, скобки) обрабатываются корректно."""
    data = [
        {"description": "Подписка (январь)"},
        {"description": "Подписка (февраль)"}
    ]
    categories = ["(январь)"]
    result = process_bank_operations(data, categories)
    expected = {"(январь)": 1}
    assert result == expected


def test_empty_description_does_not_match_any_category():
    """Проверяет, что пустое описание не увеличивает счётчики категорий."""
    data = [{"description": ""}, {"description": "Зарплата"}]
    categories = ["зарплата", "продукты"]
    result = process_bank_operations(data, categories)
    expected = {"зарплата": 1, "продукты": 0}
    assert result == expected


def test_works_with_empty_data_list():
    """Проверяет, что при пустом списке операций все категории получают 0."""
    result = process_bank_operations([], ["еда", "транспорт"])
    expected = {"еда": 0, "транспорт": 0}
    assert result == expected


def test_works_with_empty_categories_list():
    """Проверяет, что при пустом списке категорий возвращается пустой словарь."""
    data = [{"description": "Зарплата"}]
    result = process_bank_operations(data, [])
    expected = {}
    assert result == expected
