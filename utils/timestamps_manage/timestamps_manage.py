from pprint import pprint

import aioschedule
from asyncio import sleep

import asyncio
from aiogram.utils.exceptions import ChatNotFound

from data.config import DEFAULT_USERNAME
from utils.db_api.db import MarathonMembersModel, TimestampsModel, \
    ModeratorsModel, OutOfMarathonUsersModel
from loader import bot
from datetime import datetime
import time
from datetime import timedelta, datetime
from utils.motivational_phrases.phrases import get_motivational_phrase_by_marathon_day

from keyboards.inline.moderators import update_marathon_member_statistic_markup, kick_marathon_member_markup
from .utils import *


async def send_message(chat_id, message, markup=None):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=markup
        )
    except:
        ...


async def kick_from_marathon(marathon_member):
    await update_marathon_member(marathon_member, on_marathon=False, failed_days=MAX_FAILED_DAYS)
    await OutOfMarathonUsersModel.add_out_of_marathon_user(marathon_member)


async def notify_moderator_about_failed_timestamp(marathon_member):
    moderator = await ModeratorsModel.get_moderator()
    message = f"Участник {get_marathon_member_contact(marathon_member)} не вовремя прислал сегодня отчёт\n" \
              f"Свяжитесь с ним для выяснения причин и мотивирующей беседы"
    await send_message(moderator.telegram_id, message,
                       update_marathon_member_statistic_markup(marathon_member.telegram_id))


async def notify_moderator_about_failed_day(marathon_member):
    moderator = await ModeratorsModel.get_moderator()
    message = f"Участник {get_marathon_member_contact(marathon_member)} не прислал сегодня утренние сообщения. " \
              f"Свяжитесь с ним для выяснения причин и мотивирующей беседы"
    await send_message(moderator.telegram_id, message,
                       update_marathon_member_statistic_markup(marathon_member.telegram_id))


async def notify_marathon_member_about_success_first_timestamp(marathon_member):
    marathon_day = marathon_member.marathon_day
    message = get_motivational_phrase_by_marathon_day(marathon_day)
    await send_message(marathon_member.telegram_id, message[SUCCESS_FIRST_TIMESTAMP_MESSAGE_INDEX])
    await send_message(
        chat_id=marathon_member.telegram_id,
        message=f"Чтобы день был засчитан - пришли не позднее, чем "
                f"{get_second_timestamp_deadline_time(marathon_member.wakeup_time)} "
                "второй отчёт текстовым сообщением, чем полезно было твоё утро."
    )


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


async def notify_moderator_about_kick_marathon_member(marathon_member):
    moderator = await ModeratorsModel.get_moderator()
    message = f"Участник {get_marathon_member_contact(marathon_member)} " \
              f"обнулился и выбыл из чата, не завершив челленж. Свяжитесь с ним"
    await send_message(moderator.telegram_id, message,
                       kick_marathon_member_markup(marathon_member.telegram_id))
    await kick_from_marathon(marathon_member)


async def check_timestamps():
    timestamps = await TimestampsModel.get_timestamps_by_filters(datetime.now().strftime("%d.%m.%Y"), completed=False)
    for timestamp in timestamps:
        # Если прошло 70 минут с момента
        if int(time.time()) - timestamp.last_timestamp in range(-5, 6):
            marathon_member = await MarathonMembersModel.get_marathon_member_by_pk(timestamp.marathon_member_id)
            await update_timestamp(marathon_member, completed=True)
            await update_marathon_member(marathon_member, failed_days=marathon_member.failed_days + 1)
            if marathon_member.failed_days + 1 == MAX_FAILED_DAYS:
                await notify_moderator_about_kick_marathon_member(marathon_member)
            else:
                await notify_moderator_about_failed_day(marathon_member)
