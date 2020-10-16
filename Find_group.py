from aiogram.dispatcher.filters.state import StatesGroup, State


class Find_project(StatesGroup):
    F1 = State()
    F2 = State()


class Note_project(StatesGroup):
    N1 = State()
    N2 = State()


class Add_image(StatesGroup):
    I1 = State()
    I2 = State()