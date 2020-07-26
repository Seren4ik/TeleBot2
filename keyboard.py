from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnStart = KeyboardButton('/start')
btnHelp = KeyboardButton('/help')
btnStartProject = KeyboardButton('/start_project')
btnAndProject = KeyboardButton('/and_project')
btnViewProject = KeyboardButton("/view_projects")
btnCancel = KeyboardButton('/cancel')
btnReminders = KeyboardButton('/reminders')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnStart, btnHelp, btnStartProject, btnAndProject, btnCancel, btnReminders,btnViewProject)