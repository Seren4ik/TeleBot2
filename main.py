
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
import asyncio
import logging
from weather import what_weather

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
#setattr(api,"API_URL",PATCHED_URL)

loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

city = ["тамбов","дмитров","москва","дубна","ульяновск","сочи","крым","нижний новгород",
        "яхрома","вологда","алупка","симеиз","санкт-петербург","мурманск","архангельск",
        "краснодар","ростов","карелия", "астрахань","севастополь","талдом","кимры","куминово"]
swear = ["пошел на хуй","пошли на хуй","пошел на хуй!"]
swear2 = ["600 рублей"]


@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """Отправить список команд бота"""
    await message.reply(text='''Мои команды:
                             /start -- запустить бота
                             /help -- увидеть это сообщение
                             /weather -- узнать погоду
                             /currency_value -- узнать стоимость валюты
                             /drank -- ввести данные сколько выпил
                             /how_much_drank --узнать сколько выпил
                             ''', reply=False)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Приветствовать"""
    await message.reply("Привет!\nЯ - Bot")
    await send_menu(message=message)

@dp.message_handler(commands=['weather'])
async def send_weather(message: types.Message):
    """Узнать погоду"""
    await message.answer("Введите город:")


@dp.message_handler(content_types=['text'])
async def aho_bot(message: types.Message):

    text = message.text.strip().lower()
    if text in city:
        await message.reply(what_weather(text))
    elif text in swear:
        await message.answer("600 рублей")
    elif text in swear2:
        await message.answer("Пошел на хуй!")
    else: return



def main():
    executor.start_polling(
        dispatcher=dp,
    )
if __name__=="__main__":
    main()