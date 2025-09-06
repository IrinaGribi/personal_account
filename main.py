from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.masks import get_mask_card_number, get_mask_account

print (get_mask_card_number("60111111 1111 1117"))

result = mask_account_card("СЧЕТ 41111111111111112856")
date_result = get_date("2023-03-11T02:26:18.671407")
print(result)
print(date_result)


filter_result = filter_by_state([
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
])
sort_date = sort_by_date([
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
])
print(filter_result)
print(sort_date)
