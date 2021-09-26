from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Изменить время подъема 🕣"),
        ],
    ],
    resize_keyboard=True
)
