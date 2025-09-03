import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture()
def data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.mark.parametrize("expected", [([
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
])])
def test_filter_by_state(data, expected):
    """Параметризованный тест фильтрации, возвращает executed."""
    assert filter_by_state(data) == expected


@pytest.mark.parametrize("state, expected", [("CANCELED",
            [
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ])])
def test_filter_by_state_canceled(data, state, expected):
    """Параметризованный тест фильтрации по статусу CANCELED."""
    assert filter_by_state(data, state) == expected


def test_filter_empty_list():
    """Тест с пустым списком"""
    with pytest.raises(ValueError):
        filter_by_state([])


@pytest.mark.parametrize("expected",[[
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        ]])
def test_sort_by_date_without_is_reverse(data, expected):
    """Параметризованный тест сортировки в порядке убывания"""
    assert sort_by_date(data) == expected


@pytest.mark.parametrize("expected",[[
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ]])
def test_sort_by_date_is_reverse(data, expected):
    """Параметризованный тест сортировки в порядке возрастания"""
    assert sort_by_date(data, False) == expected


