import aioschedule
from asyncio import sleep

import asyncio
from aiogram.utils.exceptions import ChatNotFound
from utils.db_api.db import MarathonMembersModel, TimestampsModel, \
    ModeratorsModel, OutOfMarathonUsersModel
from loader import bot
from datetime import datetime

from keyboards.inline.moderators import update_marathon_member_statistic_markup

from .utils import times_equal, set_timestamp

BASE_SLEEP_SECONDS = 1
MIN_IN_SEC = 60
FIRST_TIMESTAMP_MINUTES = 10
LAST_TIMESTAMP_MINUTES = 60
MAX_FAILED_DAYS = 3


# Наругать пользователя
async def scold_marathon_member(marathon_member, failed_days):
    message = f"Вы пропустили сдачу отчета {failed_days} из {MAX_FAILED_DAYS}"
    try:
        await bot.send_message(
            chat_id=marathon_member.telegram_id,
            text=message
        )
    except:
        ...


async def notify_moderator_about_failed_timestamp(marathon_member, failed_days):
    moderator = await ModeratorsModel.get_moderator()
    if marathon_member.username != 'Отсутствует':
        message = f"@{marathon_member.username} пропустил сдачу отчета {failed_days}/{MAX_FAILED_DAYS}"
    else:
        message = f"Пользователь с id {marathon_member.telegram_id} " \
                  f"пропустил сдачу отчета {failed_days}/{MAX_FAILED_DAYS}"
    try:
        await bot.send_message(
            chat_id=moderator.telegram_id,
            text=message,
            reply_markup=update_marathon_member_statistic_markup(marathon_member.telegram_id)
        )
    except:
        ...


async def notify_marathon_member_about_exclude_marathon(marathon_member):
    moderator = await ModeratorsModel.get_moderator()
    try:
        message = f"Вы выбываете из марафона по ранним подъемам. Если у вас возник форс-мажор, " \
                  f"свяжитесь с модератором @{moderator.username}"
        await bot.send_message(
            chat_id=marathon_member.telegram_id,
            text=message
        )
    except:
        ...


async def kick_from_marathon(marathon_member):
    await OutOfMarathonUsersModel.add_out_of_marathon_user(marathon_member)
    await notify_marathon_member_about_exclude_marathon(marathon_member)
    await MarathonMembersModel.update_marathon_member(
        telegram_id=marathon_member.telegram_id,
        on_marathon=False
    )


async def update_marathon_member_statistic(marathon_member, failed_days):
    await MarathonMembersModel.update_marathon_member(
        telegram_id=marathon_member.telegram_id,
        failed_days=failed_days
    )
    await TimestampsModel.delete_timestamp(marathon_member)
    await scold_marathon_member(marathon_member, failed_days)
    await notify_moderator_about_failed_timestamp(marathon_member, failed_days)


async def fail_timestamp(marathon_member):
    failed_days = marathon_member.failed_days + 1
    if failed_days == MAX_FAILED_DAYS:
        await kick_from_marathon(marathon_member)
    else:
        await update_marathon_member_statistic(marathon_member, failed_days)


async def check_timestamp(marathon_member):
    await asyncio.sleep(FIRST_TIMESTAMP_MINUTES * MIN_IN_SEC)
    timestamp = await TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        if not timestamp.first_timestamp_success:
            await fail_timestamp(marathon_member)

    await asyncio.sleep(LAST_TIMESTAMP_MINUTES * MIN_IN_SEC)
    timestamp = await TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        await fail_timestamp(marathon_member)


async def add_timestamps_for_marathon_members():
    now = datetime.now()
    marathon_members = await MarathonMembersModel.get_marathon_members_by_filters(on_marathon=True)
    for member in marathon_members:
        if times_equal(now=now, user_time=member.wakeup_time, msk_timedelta=int(member.msk_timedelta)):
            await TimestampsModel.add_timestamp(
                marathon_member=member,
                first_timestamp=set_timestamp(FIRST_TIMESTAMP_MINUTES),
                last_timestamp=set_timestamp(LAST_TIMESTAMP_MINUTES)
            )
            await check_timestamp(member)


async def setup():
    aioschedule.every().hours.at(":30").do(add_timestamps_for_marathon_members)
    aioschedule.every().hours.at(":00").do(add_timestamps_for_marathon_members)

    while True:
        await aioschedule.run_pending()
        await sleep(BASE_SLEEP_SECONDS)

