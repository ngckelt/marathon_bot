from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound

from keyboards.inline.moderators import update_marathon_member_statistic_markup,\
    update_marathon_member_statistic_callback, kick_marathon_member_callback

from utils.timestamps_manage.timestamps_manage import update_marathon_member, \
    notify_marathon_member_about_success_last_timestamp

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
                text="День засчитан, несмотря на недоразумение! Челлендж продолжается. Жду тебя завтра"
            )

            # Возможно это нужно будет добавить
            # await notify_marathon_member_about_success_last_timestamp(marathon_member)
        except:
            ...
    else:
        try:
            await bot.send_message(
                chat_id=marathon_member.telegram_id,
                text="День не засчитан. Но я жду тебя завтра на продолжение челленджа. Всё получится ♥️"
            )
        except:
            ...
        text += "Не зачтено"
    await callback.message.edit_text(text)


@dp.callback_query_handler(kick_marathon_member_callback.filter())
async def kick_marathon_member(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    text = callback.message.text
    text += '\n✅ Обработано: '
    marathon_member_telegram_id = callback_data.get('member_telegram_id')
    accept = callback_data.get('accept')
    group_id = callback_data.get('group_id')

    if accept == 'False':
        marathon_member = await MarathonMembersModel.get_marathon_member(marathon_member_telegram_id)
        kick_message = f"Привет, {marathon_member.first_name} {marathon_member.last_name}! " \
                       f"Что-то пошло не так - ты обнулился и выпал из чата ранних подъёмов. " \
                       "Нам очень жаль! Ведь ты не прошел челленж до конца. Предлагаю связаться с ментором " \
                       "[имя и ссылка на юзернейм] и обсудить твоё возвращение к единомышленникам."
        try:
            await bot.kick_chat_member(group_id, marathon_member_telegram_id)
        except Exception as e:
            print(e)
            pprint(e.__dict__)

        try:
            await bot.send_message(
                chat_id=marathon_member_telegram_id,
                text=kick_message,
                reply_markup=types.ReplyKeyboardRemove()
            )
        except:
            ...
    else:
        ...

