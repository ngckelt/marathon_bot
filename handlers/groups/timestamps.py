import time

from aiogram import types
from loader import dp, bot

from filters.group_chat import IsGroup
from utils.db_api.db import MarathonMembersModel, TimestampsModel
from .utils import seconds_to_time, get_message_text_by_marathon_day


def get_second_timestamp_deadline_time(time):
    return {
        '5-00': '6:30',
        '5-30': '7:00',
        '6-00': '7:30',
    }.get(time)


async def success_first_timestamp(marathon_member):
    day = marathon_member.marathon_day
    second_timestamp_deadline_time = get_second_timestamp_deadline_time(marathon_member.wakeup_time)
    message = f"Доброе утро! День {day}\n Чтобы день был засчитан - пришли " \
              f"текстовое сообщение, чем полезно было твое утро, не позднее " \
              f"{second_timestamp_deadline_time}"
    try:
        await bot.send_message(
            chat_id=marathon_member.telegram_id,
            text=message
        )
    except:
        ...


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.VIDEO_NOTE)
async def catch_video_note(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is not None:
        timestamp = await TimestampsModel.get_timestamp(marathon_member)
        if timestamp is not None:
            if timestamp.first_timestamp - time.time() > 0:
                await TimestampsModel.update_timestamp(
                    marathon_member=marathon_member,
                    first_timestamp_success=True
                )
                await success_first_timestamp(marathon_member)


@dp.message_handler(IsGroup())
async def catch_message(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is not None:
        timestamp = await TimestampsModel.get_timestamp(marathon_member)
        if timestamp is not None:
            if timestamp.first_timestamp <= time.time() <= timestamp.last_timestamp:
                # успешно две отметки
                marathon_day = marathon_member.marathon_day + 1
                await MarathonMembersModel.update_marathon_member(
                    telegram_id=marathon_member.telegram_id,
                    marathon_day=marathon_day
                )

                await message.answer(get_message_text_by_marathon_day(marathon_day))
                await TimestampsModel.delete_timestamp(marathon_member)

                try:
                    await bot.send_message(
                        chat_id=marathon_member.telegram_id,
                        text="День засчитан! Жду тебя завтра ✨"
                    )
                except:
                    ...






