from aiogram.types  import ReplyKeyboardMarkup, KeyboardButton

b_1 = KeyboardButton('КАРТА')
b_2 = KeyboardButton('ИГРОК')


kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)

kb_menu.add(b_1, b_2)