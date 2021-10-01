import aioschedule
from asyncio import sleep

import asyncio
from aiogram.utils.exceptions import ChatNotFound
from utils.db_api.db import MarathonMembersModel, TimestampsModel, \
    ModeratorsModel, OutOfMarathonUsersModel
from loader import bot
from datetime import datetime
from keyboards.inline.moderators import update_marathon_member_statistic_markup
from utils.timestamps_manage.utils import times_equal, set_timestamp, FIRST_TIMESTAMP_MINUTES, LAST_TIMESTAMP_MINUTES
from utils.timestamps_manage.timestamps_manage import check_timestamp


async def add_timestamps_for_marathon_members():
    now = datetime.now()
    marathon_members = await MarathonMembersModel.get_marathon_members_by_filters(on_marathon=True)
    for member in marathon_members:
        if times_equal(now=now, user_time=member.wakeup_time, msk_timedelta=member.msk_timedelta):
            await TimestampsModel.add_timestamp(
                marathon_member=member,
                first_timestamp=set_timestamp(FIRST_TIMESTAMP_MINUTES),
                last_timestamp=set_timestamp(LAST_TIMESTAMP_MINUTES)
            )
            await check_timestamp(member)


