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
from Find_group import Find_project, Note_project, Add_image
from datetime import datetime, timedelta
from Valid_day import valid_day
from config import id_admin
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
    return (time_hour)


def time_2():
    city_time = datetime.utcnow() + timedelta(hours=3)
    return (city_time)


def time_3():
    time = datetime.utcnow() + timedelta(hours=3)
    project_time = time.strftime("%Y.%m.%d-%H:%M")
    return (project_time)


@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """Отправить список команд бота"""
    await message.reply(text='''Мои команды:
                             /start -- запустить бота
                             /help -- увидеть это сообщение
                             /start_project -- Начать проект 
                             /end_project -- Закончить проект 
                             /view_projects -- Показать проекты
                             /find_a_project -- Найти проект по имени или артикулу
                             /delete_project -- Удалить проект 
                             /note -- Примечание по проекту
                             /add_image -- Вставить картнику
                             /reminders -- Запустить периодичное напоминание
                             /stop -- остановить таймер
                             ''', reply=False, reply_markup=kb.greet_kb)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Приветствовать"""
    await message.reply("Привет!\nЯ - Bot")
    await send_menu(message=message)


"""___________Сохранение начала проекта________________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['start_project'], state=None)
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
    note1 = ("-")
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
            note=note1,
            text_and=text_and,
            time_start=time_3(),
            time_and=time_and
        )
        await message.answer(f"<b>Вы начали проект: {('-').join(start_project)} </b>")
        await state.finish()
    else:
        await message.answer(f"<b>Проект с таким артикулом уже есть: {code_name}</b>")
    return start_project


"""______________________Сохранение окончания проекта_________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['end_project'], state=None)
async def end_project(message: types.Message):
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
async def end_project1(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса, сохранение данных в базу"""
    projects = Db1.list_message("Sergey")
    time_and = time_3()
    text_end = "Завершен"
    code_name = message.text
    p = []
    for i in projects:
        if i[0] == code_name:
            p.append(i[0])

    if len(p) > 0:
        await message.answer(f"<b>Вы завершили проект: {code_name} </b>")
        await state.update_data(code_name=code_name)

        Db1.update_data(
            code_name=code_name,
            text_and=text_end,
            time_and=time_and
        )
        await state.finish()
    else:
        await message.answer(f"<b>Артикул не обнаружен: {code_name} </b>")
    return code_name


"""______________________Удалить проект_________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['delete_project'], state=None)
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
        if i[0] == code_name:
            p.append(i[0])

    if len(p) > 0:
        await message.answer(f"<b>Вы удалили проект: {code_name} </b>")
        await state.update_data(code_name=code_name)

        Db1.delete_message(code_name)

        await state.finish()
    else:
        await message.answer(f"<b>Артикул не обнаружен: {code_name} </b>")
    return code_name


"""______________________Найти проект по имени или артикулу_________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['find_a_project'], state=None)
async def find_a_project(message: types.Message):
    """Найти проект"""
    await message.answer("<b>Вы хотите найти проект. Введите артикул или название: </b>")
    await Find_project.next()


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()


@dp.message_handler(state=Find_project.F1)
async def find_project1(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса"""
    projects = Db1.list_message("Sergey")
    project1 = message.text
    p = []
    for i in projects:
        if project1 in i[1] or project1 in i[0]:
            p.append(i)

    if len(p):
        p1 = sorted(p, key=lambda project2: project2[2])
        for i in p1:
            await asyncio.sleep(1)
            photo1 = i[-1]
            try:
                lead_time = ((datetime.strptime(str(i[4]), "%Y.%m.%d-%H:%M")) - (
                    datetime.strptime(str(i[2]), "%Y.%m.%d-%H:%M")))
                day1 = valid_day(lead_time)
                await message.answer(f'<b>{i[0:-1]}.\n Время выполнения: {day1}</b>')
            except:
                await message.answer(f'<b>{i[0:-1]}.\n Время выполнения: - </b>')
            try:
                await message.answer_photo(photo=photo1)
            except:
                continue
        await message.answer(f'<b>Проектов: {len(p)}</b>')
        await state.finish()
    else:
        await message.answer("<b>Проект не найден, попробуйте еще раз</b>")


"""______________________Внести примечание в проект_________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['note'], state=None)
async def note_project(message: types.Message):
    """Внести примечание в проект"""
    await message.answer("<b>Вы хотите внести примечание в проект. Введите артикул: </b>")
    await Note_project.next()


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()


@dp.message_handler(state=Note_project.N1)
async def note_project1(message: types.Message, state: FSMContext):
    """Второй вопрос, примечание"""
    projects = Db1.list_message("Sergey")
    code_name = message.text
    p = []
    for i in projects:
        if code_name == i[0]:
            p.append(i)

    if len(p):
        await message.answer("<b>Введите примечание: </b>")
        await state.update_data(code_name1=code_name)
        await Note_project.next()
    else:
        await message.answer("<b>Проект не найден, попробуйте еще раз</b>")


@dp.message_handler(state=Note_project.N2)
async def note_project2(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса"""

    note1 = message.text
    data = await state.get_data()
    code_name1 = data.get('code_name1')

    Db1.note_data(
        code_name=code_name1,
        note=note1
    )

    project1 = Db1.name_message(code_name1)
    await message.answer(f"<b>{project1[0][0:-1]} </b>")
    await state.finish()


"""______________________Добавить картинку в проект_________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['add_image'], state=None)
async def add_image(message: types.Message):
    """Добавить картинку в проект"""
    await message.answer("<b>Вы хотите добавить картинку в проект. Введите артикул: </b>")
    await Add_image.next()


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отменить ввод данных"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('<b>Данные не сохранены</b>')
    await state.finish()


@dp.message_handler(state=Add_image.I1)
async def add_image1(message: types.Message, state: FSMContext):
    """Второй вопрос, примечание"""
    projects = Db1.list_message("Sergey")
    code_name = message.text
    p = []
    for i in projects:
        if code_name == i[0]:
            p.append(i)

    if len(p):
        await message.answer("<b>Добавте картинку: </b>")
        await state.update_data(code_name1=code_name)
        await Add_image.next()
    else:
        await message.answer("<b>Проект не найден, попробуйте еще раз</b>")


@dp.message_handler(state=Add_image.I2, content_types=types.ContentType.PHOTO)
async def add_image2(message: types.Message, state: FSMContext):
    """Второй вопрос, завершение опроса"""

    image1 = message.photo[-1].file_id
    data = await state.get_data()
    code_name1 = data.get('code_name1')

    Db1.image_data(
        code_name=code_name1,
        image=image1
    )

    project1 = Db1.name_message(code_name1)
    for i in project1:
        await message.answer(f"<b>{i[0:-1]} </b>")
        await message.answer_photo(photo=i[-1])

    await state.finish()


"""______________________Посмотреть проекты_________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['view_projects'])
async def view_projects(message: types.Message):
    """Посмотреть проекты"""
    projects = Db1.list_message("Sergey")
    projects1 = sorted(projects, key=lambda project2: project2[2])
    date1 = projects1[0][2]
    count_projects = 0
    for i in projects1:
        count_projects += 1
        await message.answer(f"<b>{i[0:-1]}</b>")
    await message.answer(f"<b>Количество проектов начиная с {date1} : {count_projects}</b>")


"""__________________________Напоминания________________________________________________________________"""


@dp.message_handler(user_id=id_admin, commands=['reminders'], state=None)
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
        await message.reply(
            f"<b>Установлено напоминание:{answer3}, промежуток(Ч.М.С): {gap_time}, кол-во повторений:{answer5} </b>")
        await state.finish()
        time_start = time_2()
        for i in range(0, answer5 + 1):
            time_2()
            time_delta = (time_2() - time_start)
            #            print(time_delta)
            if time_delta > timedelta(seconds=answer4):
                await sms(answer3)
            await asyncio.sleep(answer4)


@dp.message_handler()
async def sms(text):
    await bot.send_message(chat_id="1268358424", text=f"<b>{text}</b>")


def main():
    executor.start_polling(
        dispatcher=dp, )


if __name__ == "__main__":
    main()
