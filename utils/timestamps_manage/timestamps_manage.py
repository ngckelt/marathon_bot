import aioschedule
from asyncio import sleep

import asyncio
from aiogram.utils.exceptions import ChatNotFound
from utils.db_api.db import MarathonMembersModel, TimestampsModel, \
    ModeratorsModel, OutOfMarathonUsersModel
from loader import bot
from datetime import datetime
import time
from datetime import timedelta, datetime
from utils.motivational_phrases.phrases import get_motivational_phrase_by_marathon_day

from keyboards.inline.moderators import update_marathon_member_statistic_markup, kick_marathon_member_markup
from .utils import *


# Наругать пользователя
# async def scold_marathon_member(marathon_member, failed_days):
#     message = f"Вы пропустили сдачу отчета {failed_days} из {MAX_FAILED_DAYS}"
#     try:
#         await bot.send_message(
#             chat_id=marathon_member.telegram_id,
#             text=message
#         )
#     except:
#         ...
#
#
# async def notify_moderator_about_failed_timestamp(marathon_member, failed_days):
#     moderator = await ModeratorsModel.get_moderator()
#     if marathon_member.username != 'Отсутствует':
#         message = f"@{marathon_member.username} пропустил сдачу отчета {failed_days}/{MAX_FAILED_DAYS}"
#     else:
#         message = f"Пользователь с id {marathon_member.telegram_id} " \
#                   f"пропустил сдачу отчета {failed_days}/{MAX_FAILED_DAYS}"
#     try:
#         await bot.send_message(
#             chat_id=moderator.telegram_id,
#             text=message,
#             reply_markup=update_marathon_member_statistic_markup(marathon_member.telegram_id)
#         )
#     except:
#         ...
#
#
# async def notify_marathon_member_about_exclude_marathon(marathon_member):
#     moderator = await ModeratorsModel.get_moderator()
#     try:
#         message = f"Вы выбываете из марафона по ранним подъемам. Если у вас возник форс-мажор, " \
#                   f"свяжитесь с модератором @{moderator.username}"
#         await bot.send_message(
#             chat_id=marathon_member.telegram_id,
#             text=message
#         )
#     except:
#         ...
#
#
# async def update_marathon_member_statistic(marathon_member, failed_days):
#     await MarathonMembersModel.update_marathon_member(
#         telegram_id=marathon_member.telegram_id,
#         failed_days=failed_days
#     )
#     await TimestampsModel.delete_timestamp(marathon_member)
#     await scold_marathon_member(marathon_member, failed_days)
#     await notify_moderator_about_failed_timestamp(marathon_member, failed_days)
#
#
def get_second_timestamp_deadline_time(time):
    return {
        '5-00': '6:30',
        '5-30': '7:00',
        '6-00': '7:30',
    }.get(time)


def get_first_timestamp_deadline_time(time):
    return {
        '5-00': '6:10',
        '5-30': '5:40',
        '6-00': '6:10',
    }.get(time)


async def send_message(chat_id, message, markup=None):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=markup
        )
    except:
        ...


async def notify_moderator_about_failed_timestamp(marathon_member):
    moderator = await ModeratorsModel.get_moderator()
    if marathon_member.username != 'Отсутствует':
        message = f"Участник @{marathon_member.username} не вовремя прислал сегодня отчёт\n" \
                  f"Свяжитесь с ним для выяснения причин и мотивирующей беседы"
    else:
        message = f"Участник {marathon_member.phone} не вовремя прислал сегодня отчёт\n" \
                  f"Свяжитесь с ним для выяснения причин и мотивирующей беседы"
    await send_message(moderator.telegram_id, message,
                       update_marathon_member_statistic_markup(marathon_member.telegram_id))


async def notify_moderator_about_failed_day(marathon_member):
    moderator = await ModeratorsModel.get_moderator()
    marathon_member_contacts = f"{marathon_member.first_name} {marathon_member.last_name} "
    if marathon_member.username != 'Отсутствует':
        marathon_member_contacts += f"@{marathon_member.username}"
    else:
        marathon_member_contacts += f"@{marathon_member.phone}"
    message = f"Участник {marathon_member_contacts} не прислал сегодня утренние сообщения. " \
              f"Свяжитесь с ним для выяснения причин и мотивирующей беседы"
    await send_message(moderator.telegram_id, message,
                       update_marathon_member_statistic_markup(marathon_member.telegram_id))


async def notify_marathon_member_about_success_first_timestamp(marathon_member):
    marathon_day = marathon_member.marathon_day
    message = get_motivational_phrase_by_marathon_day(marathon_day)
    await send_message(marathon_member.telegram_id, message[SUCCESS_FIRST_TIMESTAMP_MESSAGE_INDEX])


async def notify_marathon_member_about_success_last_timestamp(marathon_member):
    marathon_day = marathon_member.marathon_day
    message = get_motivational_phrase_by_marathon_day(marathon_day)
    await send_message(marathon_member.telegram_id, message[SUCCESS_LAST_TIMESTAMP_MESSAGE_INDEX])


async def notify_marathon_member_about_fail_first_timestamp(marathon_member):
    message = f"Это действие должно быть выполнено до " \
              f"{get_second_timestamp_deadline_time(marathon_member.wakeup_time)}. " \
              f"У вас пропуск. Всего возможно 3 пропуска. " \
              "Сейчас вы можете дальше продолжить челленж"
    await send_message(marathon_member.telegram_id, message)


async def notify_marathon_member_about_fail_day(marathon_member):
    message = "День не засчитан. Но я жду тебя завтра на продолжение челленджа. Всё получится ♥️."
    await send_message(marathon_member.telegram_id, message)


async def update_timestamp(marathon_member, **update_data):
    await TimestampsModel.update_timestamp(marathon_member, **update_data)


async def update_marathon_member(marathon_member, **update_data):
    await MarathonMembersModel.update_marathon_member(marathon_member.telegram_id, **update_data)


async def check_timestamp(marathon_member):
    await asyncio.sleep(LAST_TIMESTAMP_MINUTES * MIN_IN_SEC)
    timestamp = await TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        await update_marathon_member(marathon_member, failed_days=marathon_member.failed_days + 1)
        if marathon_member.failed_days + 1 == MAX_FAILED_DAYS:
            await notify_moderator_about_kick_marathon_member(marathon_member, 'тут будет id группы')
        else:
            await notify_moderator_about_failed_day(marathon_member)


async def notify_moderator_about_kick_marathon_member(marathon_member, group_id):
    moderator = await ModeratorsModel.get_moderator()
    marathon_member_contacts = f"{marathon_member.first_name} {marathon_member.last_name} "
    if marathon_member.username != 'Отсутствует':
        marathon_member_contacts += f"@{marathon_member.username}"
    else:
        marathon_member_contacts += f"@{marathon_member.phone}"
    message = f"Участник {marathon_member_contacts} обнулился и выбыл из чата, не завершив челленж. Свяжитесь с ним"
    await send_message(moderator.telegram_id, message,
                       kick_marathon_member_markup(marathon_member.telegram_id, group_id))


# async def success_last_timestamp(marathon_member):
#     marathon_day = marathon_member.marathon_day + 1
#     message = get_motivational_phrase_by_marathon_day(marathon_day)
#     try:
#         await bot.send_message(
#             chat_id=marathon_member.telegram_id,
#             text=message[1]
#         )
#     except:
#         ...
#
#
# def get_first_timestamp_deadline(marathon_member):
#     return {
#         '5-00': '5:10',
#         '5-30': '5:40',
#         '6-00': '6:10',
#     }.get(marathon_member.wakeup_time)
#
#
# async def fail_first_timestamp(marathon_member):
#     message = f"Это действие должно быть выполнено до {get_first_timestamp_deadline(marathon_member)}. У вас пропуск. Всего возможно 3 пропуска. " \
#               "Сейчас вы можете дальше продолжить челленж"
#     try:
#         await bot.send_message(
#             chat_id=marathon_member.telegram_id,
#             text=message
#         )
#     except:
#         ...
#
#
#
#
# async def fail_timestamp(marathon_member):
#     moderator = await ModeratorsModel.get_moderator()
#     try:
#         member_data = f"{marathon_member.first_name} {marathon_member.last_name} "
#         if marathon_member.username != "Отсутствует":
#             member_data += f"@{marathon_member.username}"
#         else:
#             member_data += f"@{marathon_member.phone}"
#         message = f"Участник {member_data} не прислал сегодня утренние сообщения. " \
#                   "Свяжитесь с ним для выяснения причин и мотивирующей беседы"
#
#         await bot.send_message(
#             chat_id=moderator.telegram_id,
#             text=message,
#             reply_markup=update_marathon_member_statistic_markup(marathon_member.telegram_id)
#         )
#     except:
#         ...
#     # failed_days = marathon_member.failed_days + 1
#     # if failed_days == MAX_FAILED_DAYS:
#     #     await kick_from_marathon(marathon_member)
#     # else:
#     #     await update_marathon_member_statistic(marathon_member, failed_days)
#
#
# async def kick_from_marathon(marathon_member):
#     await OutOfMarathonUsersModel.add_out_of_marathon_user(marathon_member)
#     await notify_marathon_member_about_exclude_marathon(marathon_member)
#     await MarathonMembersModel.update_marathon_member(
#         telegram_id=marathon_member.telegram_id,
#         on_marathon=False
#     )



