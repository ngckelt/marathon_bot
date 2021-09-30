from pprint import pprint

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_markup(row_width, *text_options):
    keyboard = []
    btn_quantity = len(text_options)
    i = 0
    while btn_quantity:
        buttons = []
        for _ in range(row_width):
            try:
                buttons.append(KeyboardButton(text_options[i]))
                i += 1
                btn_quantity -= 1
            except IndexError:
                continue
        keyboard.append(buttons)

    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return markup

