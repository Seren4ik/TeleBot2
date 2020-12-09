from datetime import datetime

# difference_bed = ((datetime.strptime(str("2019.11.10-12:17"), "%Y.%m.%d-%H:%M")) - (
#     datetime.strptime(str("2019.10.15-10:44"), "%Y.%m.%d-%H:%M")))


def valid_day(x):
    list1 = ['2', '3', '4', '22', '23', '24', '32', '33', '34', '42']
    list2 = ['1', '21', '31', '41', '51', '61', '71']

    if str(x)[0] in list1:
        return (str(x).replace('days', 'Дня'))
    elif str(x)[0] in list2:
        return (str(x).replace('day', 'День'))
    elif str(x)[0] not in list1 and list2:
        return (str(x).replace('days', 'Дней'))


# print(valid_day(difference_bed))
# print(str(difference_bed)[0])
