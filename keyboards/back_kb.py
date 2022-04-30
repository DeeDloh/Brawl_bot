from aiogram.types  import ReplyKeyboardMarkup, KeyboardButton

b_1 = KeyboardButton('НАЗАД')

kb_back = ReplyKeyboardMarkup(resize_keyboard=True)

kb_back.add(b_1)