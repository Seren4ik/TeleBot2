from datetime import datetime, timedelta
from time import *
import asyncio


def time_1():
    city_time = datetime.utcnow() + timedelta(hours=3)
    return(city_time)


async def valid(text):
    data = text.split(".")
    data2 = data[2].split("-")
    hours = int(data[0])
    minutes = int(data[1])
    seconds = int(data2[0])
    print(hours,minutes,seconds)
    await time_2(hours=hours,minutes=minutes,seconds=seconds)


async def time_2(hours,minutes,seconds):
    time_start = datetime.utcnow() + timedelta(hours=3)
    second = ((hours*3600)+(minutes*60)+seconds)
    print(second)

    while True:
        time_1()
        await asyncio.sleep(second)
        time_delta =(time_1() - time_start)
        #print(time_delta)
        if time_delta > timedelta(seconds=second):
            await sms("ererg")


async def sms(text):
    print(text + time_1().strftime("%H:%M:%S"))


loop = asyncio.get_event_loop()
loop.create_task(valid(input("Введите интервал:")))
loop.run_forever()