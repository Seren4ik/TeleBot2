from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
import asyncio
import keyboard as kb
from valid_time import valid, valid2
from valid_start_project import valid_start
import Db1
from States_group import drink
from Group_project import project
from Delete_group import delproject
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
                             /start_project -- Начать проект 
                             /and_project -- Закончить проект 
                             /view_projects -- Посмотреть проекты
                             /delete_project -- Удалить проект 
                             /reminders -- Запустить периодичное напоминание
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
    await message.answer("<b>Вы начинаете проект. Введите артикул и название в формате(Артикул-название): </b>")
    await project.first()


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
    start_project = valid_start(message.text)
    if start_project == "Не правильный формат":
        await message.reply("<b>Не правильный формат, введите через (-)</b>")
        return start_project
    code_name = start_project[0]
    project_name = start_project[1]
    projects = Db1.list_message("Sergey")
    text_and = ("-")
    time_and = ("-")
    p = []
    for i in projects:
        if i[1] == code_name:
            p.append(i[1])

    if len(p) == 0:
        await state.update_data(start_project=start_project)
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
    else: await message.answer(f"<b>Проект с таким артикулом уже есть: {code_name}</b>")
    return start_project



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
    time_and = time_3()
    text_and = "Завершен"
    code_name = message.text
    p = []
    for i in projects:
        if i[1] == code_name:
            p.append(i[1])

    if len(p) > 0:
        await message.answer(f"<b>Вы закончили проект: {code_name} </b>")
        await state.update_data(code_name=code_name)

        Db1.update_data(
            code_name=code_name,
            text_and=text_and,
            time_and=time_and
        )
        await state.finish()
    else: await message.answer(f"<b>Артикул не обнаружен: {code_name} </b>")
    return code_name


"""______________________Удалить проект_________________________________________________________________"""

@dp.message_handler(commands=['delete_project'],state=None)
async def delete_project(message: types.Message):
    """Удалить проект"""
    await message.answer("<b>Вы хотите удалить проект. Введите артикул: </b>")
    await delproject.next()

@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()

@dp.message_handler(state=delproject.R1)
async def delete_project1(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса, удаление проекта"""
    projects = Db1.list_message("Sergey")
    code_name = message.text
    p = []
    for i in projects:
        if i[1] == code_name:
            p.append(i[1])

    if len(p) > 0:
        await message.answer(f"<b>Вы удалили проект: {code_name} </b>")
        await state.update_data(code_name=code_name)

        Db1.delete_message(code_name)

        await state.finish()
    else: await message.answer(f"<b>Артикул не обнаружен: {code_name} </b>")
    return code_name


"""______________________Посмотреть проекты_________________________________________________________________"""

@dp.message_handler(commands=['view_projects'])
async def view_projects(message: types.Message):
    """Посмотреть проекты"""
    projects = Db1.list_message("Sergey")
    #await message.answer(projects)
    count_projects = 0
    for i in projects:
        count_projects += 1
        await message.answer(f"<b>{i}</b>")
    await message.answer(f"<b>Количество проектов: {count_projects}</b>")

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
    await message.reply("<b>Укажите временной промежуток и кол-во повторений в формате:(Ч.М.С-X)</b>")
    await state.update_data(answer3=answer3)
    await drink.next()

@dp.message_handler(state=drink.Q2)
async def reminders(message: types.Message, state: FSMContext):
    """Достать переменые"""
    data = await state.get_data()
    answer3 = data.get("answer3")
    answer4 = valid(message.text)
    answer5 = valid2(message.text)
    answer6 = message.text.split("-")
    gap_time = answer6[0]
    if answer4 == "Не верный формат":
        await message.reply("<b>Не верный формат!</b>")
        return answer4
    elif answer5 == "Не верный формат":
        await message.reply("<b>Не верный формат!</b>")
        return answer5
    else:
        await message.reply(f"<b>Установлено напоминание:{answer3}, промежуток(Ч.М.С): {gap_time}, кол-во повторений:{answer5} </b>")
        await state.finish()
        time_start = time_2()
        for i in range(0, answer5+1):
            time_2()
            time_delta = (time_2() - time_start)
#            print(time_delta)
            if time_delta > timedelta(seconds=answer4):
                await sms(answer3)
            await asyncio.sleep(answer4)


@dp.message_handler()
async def sms(text):
    await bot.send_message(chat_id="1268358424",text=f"<b>{text}</b>")

def main():
    executor.start_polling(
        dispatcher=dp, )

if __name__=="__main__":
    main()