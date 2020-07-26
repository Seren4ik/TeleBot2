from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
import asyncio
import keyboard as kb
from validate import validate_answer
import Db1
from States_group import drink
from Group_project import project
from datetime import datetime, timedelta
from time import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)


def time_1():
    city_time = datetime.utcnow() + timedelta(hours=3)
    time_hour = city_time.strftime("%H:%M:%S")
    return(time_hour)

def time_2():
    city_time = datetime.utcnow() + timedelta(hours=3)
    return(city_time)

def time_3():
    time = datetime.utcnow() + timedelta(hours=3)
    project_time = time.strftime("%Y.%m.%d-%H:%M")
    return(project_time)

@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """Отправить список команд бота"""
    await message.reply(text='''Мои команды:
                             /start -- запустить бота
                             /help -- увидеть это сообщение
                             /start_project -- начал проект
                             /and_project -- закончил проект
                             /view_projects -- посмотреть проекты
                             /reminders -- запустить периодичное напоминание
                             /stop -- остановить таймер
                             ''', reply=False, reply_markup=kb.greet_kb)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Приветствовать"""
    await message.reply("Привет!\nЯ - Bot")
    await send_menu(message=message)

"""___________Сохранение начала проекта________________________________________________________________________"""

@dp.message_handler(commands=['start_project'],state=None)
async def start_project(message: types.Message):
    """Начать проект"""
    await message.answer("<b>Вы начали проект. Введите артикул и название: </b>")
    await project.next()


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()

@dp.message_handler(state=project.U1)
async def start_project1(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса, сохранение данных в базу"""
    user = message.from_user.id
    user2 = message.from_user.full_name
    start_project = (message.text).split("-")
    code_name = start_project[0]
    project_name = start_project[1]
    if start_project is None:
        await message.reply("<b>Введи текст или нажмите /cancel:</b>")
        return start_project
    await state.update_data(start_project=start_project)
    projects = Db1.list_message("Sergey")
    text_and = ("-")
    time_and = ("-")
    p = []
    for i in projects:
        if i[1] == code_name:
            p.append(i[1])

    if len(p) == 0:
        Db1.add_message(
            user_id=user,
            first_name=user2,
            code_name=code_name,
            text_start=project_name,
            text_and=text_and,
            time_start=time_3(),
            time_and=time_and
        )
        await message.answer(f"<b>Вы начали проект: {('-').join(start_project)} </b>")
        await state.finish()
    else: await message.answer(f"<b>Проект с таким артикулом уже есть: {code_name}. Начните заново</b>")
    await state.finish()


"""______________________Сохранение окончания проекта_________________________________________________________________"""

@dp.message_handler(commands=['and_project'],state=None)
async def and_project(message: types.Message):
    """Закончить проект"""
    await message.answer("<b>Вы заканчиваете проект. Введите артикул: </b>")
    await project.last()

@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()

@dp.message_handler(state=project.U2)
async def and_project1(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса, сохранение данных в базу"""
    projects = Db1.list_message("Sergey")
    code_name = (message.text)
    if code_name is None:
        await message.reply("<b>Введи текст или нажмите /cancel:</b>")
        return code_name
    await state.update_data(code_name=code_name)
    time_and = time_3()
    text_and = "Завершен"

    Db1.update_data(
        code_name=code_name,
        text_and=text_and,
        time_and=time_and
    )
    p = []
    for i in projects:
        if i[1] == code_name:
            p.append(i[1])

    if len(p) > 0:
        await message.answer(f"<b>Вы закончили проект: {code_name} </b>")
    else: await message.answer(f"<b>Артикул не обнаружен: {code_name} </b>")
    await state.finish()

"""______________________Посмотреть проекты_________________________________________________________________"""

@dp.message_handler(commands=['view_projects'])
async def view_projects(message: types.Message):
    """Посмотреть проекты"""
    projects = Db1.list_message("Sergey")
    #await message.answer(projects)
    for i in projects:
        await message.answer(f"<b>{i}</b>")

"""__________________________Напоминания________________________________________________________________"""

@dp.message_handler(commands=['reminders'],state=None)
async def start_reminders(message: types.Message):
    """Запустить таймер, первый вопрос"""
    await message.answer("<b>Вы запустили напоминания. Введите текст напоминания: </b>")
    await drink.next()

@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()

@dp.message_handler(state=drink.Q1)
async def reminders(message: types.Message, state: FSMContext):
    """Второй вопрос"""
    answer3 = (message.text)
    if answer3 is None:
        await message.reply("<b>Введи текст или нажмите /cancel:</b>")
        return answer3
    await message.reply("<b>Укажите периодичность в формате (Ч:М:С)</b> ")
    await state.update_data(answer3=answer3)
    await drink.next()

@dp.message_handler(state=drink.Q2)
async def reminders(message: types.Message, state: FSMContext):
    """Достать переменые"""
    data = await state.get_data()
    answer3 = data.get("answer3")
    answer4 = validate_answer(message.text)
    if answer4 is None:
        await message.reply("Введи число ДЕГЕНЕРАТ, если число дробное - введи его через точку:")
        return answer4
    await message.reply(f"Установлено напоминание:({answer3}), периодичность: {answer4} ")
    await state.finish()

    time_start = datetime.utcnow() + timedelta(hours=3)
    while True:
        time_1()
        await asyncio.sleep(answer4)
        time_delta = (time_2() - time_start).total_seconds()
        #print(time_delta)
        if time_delta > answer4:
            await sms(answer3)


@dp.message_handler()
async def sms(text):

    await bot.send_message(chat_id="1268358424",text=f"<b>{text}</b>")



def main():
    executor.start_polling(
        dispatcher=dp, )

if __name__=="__main__":
    main()