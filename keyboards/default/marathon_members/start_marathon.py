from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_marathon_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Начать челлендж"),
        ],
    ],
    resize_keyboard=True
)
