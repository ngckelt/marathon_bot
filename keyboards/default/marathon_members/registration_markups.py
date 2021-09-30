from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


request_contact_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер телефона 📞",
                           request_contact=True)
        ],
    ],
    resize_keyboard=True
)
