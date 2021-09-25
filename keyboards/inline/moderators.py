from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

update_marathon_member_statistic_callback = CallbackData('update_statistic', 'member_telegram_id', 'accept')


def update_marathon_member_statistic_markup(member_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Засчитать отсчет",
            callback_data=update_marathon_member_statistic_callback.new(member_id, "True")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Не засчитывать отчет",
            callback_data=update_marathon_member_statistic_callback.new(member_id, "False")
        )
    )
    return markup

