

def valid(text):
    try:
        data = text.split(".")
        data2 = data[2].split("-")
        hours = int(data[0])
        minutes = int(data[1])
        seconds = int(data2[0])
        seconds_timer = ((hours*3600)+(minutes*60)+seconds)
#       print(hours,minutes,seconds)
#       print(seconds_timer)
        return seconds_timer
    except: return ("Не верный формат")

def valid2(text):
    try:
        data2 = text.split("-")

        return int(data2[1])
    except: return ("Не верный формат")

# print(valid("1.30.0-3"))
# print(valid2("0.0.5-3"))





