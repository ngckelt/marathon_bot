import aioschedule
from asyncio import sleep

import asyncio
from aiogram.utils.exceptions import ChatNotFound
from utils.db_api.db import MarathonMembersModel, TimestampsModel, ModeratorsModel
from loader import bot
from datetime import datetime, timedelta

from keyboards.inline.moderators import update_marathon_member_statistic_markup

from .utils import times_equal, set_timestamp

BASE_SLEEP_SECONDS = 1
MIN_IN_SEC = 60
FIRST_TIMESTAMP_MINUTES = 10
LAST_TIMESTAMP_MINUTES = 70


async def check_first_timestamp(marathon_member):
    await asyncio.sleep(FIRST_TIMESTAMP_MINUTES)


async def check_last_timestamp(marathon_member):
    await asyncio.sleep(LAST_TIMESTAMP_MINUTES)


# Наругать пользователя
async def scold_marathon_member(marathon_member, failed_days):
    message = f"Вы пропустили сдачу отчета {failed_days} из 3"
    try:
        bot.send_message(
            chat_id=marathon_member.telegram_id,
            message=message
        )
    except ChatNotFound:
        ...


# Похвалить пользователя
async def praise_marathon_member(marathon_member, marathon_day):
    if marathon_day == 1:
        message = "Поздравляю с первым подъемом"
    elif marathon_day == 7 or marathon_day == 30:
        message = "Поздравляю, ты ближе к цели"
    else:
        message = f"Ты молодец, задание засчитано, ты уже сделал {marathon_day}/60"

    try:
        await bot.send_message(
            chat_id=marathon_member.telegram_id,
            message=message
        )
    except ChatNotFound:
        ...


async def notify_moderator_about_failed_timestamp(marathon_member):
    moderator = ModeratorsModel.get_moderator()
    message = f"{marathon_member.username} пропустил сдачу отчета {marathon_member.failed_days}/3"
    await bot.send_message(
        chat_id=moderator.telegram_id,
        message=message,
        reply_markup=update_marathon_member_statistic_markup(marathon_member.telegram_id)
    )


async def timestamp_complete(marathon_member):
    marathon_day = marathon_member.marathon_day + 1
    await MarathonMembersModel.update_marathon_member(
        marathon_member.telegram_id,
        marathon_day=marathon_day
    )
    await praise_marathon_member(marathon_member, marathon_day)


async def timestamp_failed(marathon_member):
    failed_days = marathon_member.failed_days
    await scold_marathon_member(marathon_member, failed_days)
    if failed_days < 3:
        ...
    else:
        # send_to_moderators
        # ban_user
        # remove from marathon
        ...


async def check_timestamps(marathon_member):
    await asyncio.sleep(LAST_TIMESTAMP_MINUTES * MIN_IN_SEC)
    timestamp = TimestampsModel.get_timestamp_by_marathon_member(marathon_member)
    if timestamp.first_timestamp_success and timestamp.last_timestamp_success:
        await timestamp_complete(marathon_member)
    else:
        await timestamp_failed(marathon_member)
    await TimestampsModel.delete_timestamp(timestamp.pk)


async def add_timestamps_for_marathon_members():
    now = datetime.now()
    marathon_members = await MarathonMembersModel.get_marathon_members()
    for member in marathon_members:
        if times_equal(now, member.wakeup_time, member.msk_timedelta):
            await TimestampsModel.add_timestamp(
                marathon_member=member,
                day=member.marathon_day,
                first_timestamp=set_timestamp(FIRST_TIMESTAMP_MINUTES),
                last_timestamp=set_timestamp(LAST_TIMESTAMP_MINUTES)
            )
            await check_timestamps(member)


async def setup():
    # aioschedule.every().hours.at(":30").do(send_quantums)

    while True:
        await aioschedule.run_pending()
        await sleep(BASE_SLEEP_SECONDS)

