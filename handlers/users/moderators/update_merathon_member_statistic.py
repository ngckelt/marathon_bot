from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound

from keyboards.inline.moderators import update_marathon_member_statistic_markup,\
    update_marathon_member_statistic_callback

from loader import dp
from loader import bot

from utils.db_api.db import MarathonMembersModel


@dp.callback_query_handler(update_marathon_member_statistic_callback.filter())
async def update_marathon_member_statistic(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    text = callback.message.text
    text += '\n✅ Обработано: '
    marathon_member_telegram_id = callback_data.get('member_telegram_id')
    accept = callback_data.get('accept')
    marathon_member = await MarathonMembersModel.get_marathon_member(marathon_member_telegram_id)
    if accept == 'True':
        text += "Зачтено"
        await MarathonMembersModel.update_marathon_member(
            telegram_id=marathon_member_telegram_id,
            marathon_day=marathon_member.marathon_day + 1,
            failed_days=marathon_member.failed_days - 1
        )
        try:
            await bot.send_message(
                chat_id=marathon_member.telegram_id,
                text="Модератор зачел тебе пропущенный день!"
            )
        except ChatNotFound:
            ...
    else:
        text += "Не зачтено"
    await callback.message.edit_text(text)


