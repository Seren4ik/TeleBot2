from datetime import datetime

# difference_bed = ((datetime.strptime(str("2020.10.14-10:05"), "%Y.%m.%d-%H:%M")) - (
#     datetime.strptime(str("2020.10.13-09:39"), "%Y.%m.%d-%H:%M")))


def valid_day(x):
    list1 = ['2', '3', '4', '22', '23', '24', '32', '33', '34', '42']
    list2 = ['1', '21', '31', '41', '51', '61', '71']

    if str(x)[0] in list1:
        return (str(x).replace('days', 'Дня'))
    elif str(x)[0] in list2:
        return (str(x).replace('day', 'День'))
    else:
        return (str(x).replace('days', 'Дней'))


# print(valid_day(difference_bed))
