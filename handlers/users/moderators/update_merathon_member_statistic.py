from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.moderators import update_marathon_member_statistic_markup,\
    update_marathon_member_statistic_callback

from loader import dp

from utils.db_api.db import MarathonMembersModel


@dp.message_handler(update_marathon_member_statistic_callback.filter())
async def update_marathon_member_statistic(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    text = callback.message.text + "\n\nНовый текст"
    marathon_member_telegram_id = callback_data.get('member_telegram_id')
    accept = callback_data.get('accept')
    marathon_member = MarathonMembersModel.get_marathon_member()
    if accept == 'True':
        await MarathonMembersModel.update_marathon_member(
            telegram_id=marathon_member_telegram_id,
            marathon_day=marathon_member.marathon_day + 1,
            failed_days=marathon_member.failed_days - 1
        )
    else:
        ...
    await callback.message.edit_text(text)


