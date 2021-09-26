from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData('yes_or_no', 'action', 'choice')


def yes_or_no_markup(action):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Да",
            callback_data=yes_or_no_callback.new(action, 'yes')
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Нет",
            callback_data=yes_or_no_callback.new(action, 'no')
        )
    )
    return markup
