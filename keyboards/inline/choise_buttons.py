from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать проект", callback_data="start_project"),
            InlineKeyboardButton(text="Закончить проект", callback_data="end_project"),
            InlineKeyboardButton(text="Количество проектов", callback_data="view_projects"),
        ],

        [
            InlineKeyboardButton(text="Найти проект по имени или артикулу", callback_data="find_a_project"),
            InlineKeyboardButton(text="Примечание по проекту", callback_data="note"),
            InlineKeyboardButton(text="Вставить картинку", callback_data="add_image"),
        ],
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel"),
        ]
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel"),
        ]
    ])