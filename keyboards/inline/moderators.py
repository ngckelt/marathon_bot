from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

update_marathon_member_statistic_callback = CallbackData('update_statistic', 'member_telegram_id', 'accept')
kick_marathon_member_callback = CallbackData('kick_marathon_member', 'member_telegram_id', 'group_id', 'accept')


def update_marathon_member_statistic_markup(member_telegram_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Засчитать отчет",
            callback_data=update_marathon_member_statistic_callback.new(member_telegram_id, "True")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Не засчитывать отчет",
            callback_data=update_marathon_member_statistic_callback.new(member_telegram_id, "False")
        )
    )
    return markup


def kick_marathon_member_markup(member_telegram_id, group_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Засчитать отсчет",
            callback_data=kick_marathon_member_callback.new(member_telegram_id, group_id, "True")
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Не засчитывать отчет",
            callback_data=kick_marathon_member_callback.new(member_telegram_id, group_id, "False")
        )
    )
    return markup


