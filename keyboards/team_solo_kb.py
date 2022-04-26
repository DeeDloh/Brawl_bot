from aiogram.types  import ReplyKeyboardMarkup, KeyboardButton

b_1 = KeyboardButton('ТИМ')
b_2 = KeyboardButton('СОЛО')
b_3 = KeyboardButton('НАЗАД')

kb_ts = ReplyKeyboardMarkup(resize_keyboard=True)

kb_ts.add(b_1, b_2).row(b_3)