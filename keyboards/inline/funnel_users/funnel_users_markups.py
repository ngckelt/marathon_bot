from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def instagram_link_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="@Love.skabelina",
            url="https://www.instagram.com/love.skabelina/"
        )
    )
    return markup


