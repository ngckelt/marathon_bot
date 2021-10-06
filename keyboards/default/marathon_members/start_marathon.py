from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_marathon_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Начать марафон"),
        ],
    ],
    resize_keyboard=True
)
