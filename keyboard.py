from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnStart = KeyboardButton('/start')
btnHelp = KeyboardButton('/help')
btnStartProject = KeyboardButton('/start_project')
btnEndProject = KeyboardButton('/end_project')
btnViewProject = KeyboardButton("/view_projects")
btnFindProject = KeyboardButton("/find_a_project")
btnDelProject = KeyboardButton("/delete_project")
btnNoteProject = KeyboardButton("/note")
btnImageProject = KeyboardButton("/add_image")
btnCancel = KeyboardButton('/cancel')
btnReminders = KeyboardButton('/reminders')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnStart, btnHelp, btnStartProject,
                                 btnEndProject, btnCancel, btnReminders, btnViewProject, btnDelProject, btnFindProject,
                                                                                 btnNoteProject, btnImageProject)