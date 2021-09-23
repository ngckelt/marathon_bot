from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import AVAILABLE_WAKEUP_TIMESTAMPS


wakeup_time_callback = CallbackData('wakeup_time', 'wakeup_time')


def wakeup_time_markup():
    markup = InlineKeyboardMarkup()
    for timestamp in AVAILABLE_WAKEUP_TIMESTAMPS:
        markup.add(
            InlineKeyboardButton(
                text=timestamp,
                callback_data=wakeup_time_callback.new(timestamp)
            )
        )
    return markup

