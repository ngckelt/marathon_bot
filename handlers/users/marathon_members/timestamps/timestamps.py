import time

from aiogram import types
from loader import dp

from utils.db_api.db import MarathonMembersModel, TimestampsModel
from .utils import seconds_to_time, get_message_text_by_marathon_day


@dp.message_handler(content_types=types.ContentTypes.VIDEO_NOTE)
async def catch_video_note(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    timestamp = await TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        if timestamp.first_timestamp - time.time() > 0:
            await TimestampsModel.update_timestamp(
                marathon_member=marathon_member,
                first_timestamp_success=True
            )
            await message.answer("Отлично! Видеосообщение засчитано")
    else:
        await message.answer("Таймстемпа нету")


@dp.message_handler()
async def catch_message(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    timestamp = await TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        if not timestamp.first_timestamp_success:
            await message.answer("Возможно, ты хотел отправить видеосообщение?")

        elif timestamp.first_timestamp <= time.time() <= timestamp.last_timestamp:
            marathon_day = marathon_member.marathon_day + 1
            await MarathonMembersModel.update_marathon_member(
                telegram_id=marathon_member.telegram_id,
                marathon_day=marathon_day
            )

            await message.answer(get_message_text_by_marathon_day(marathon_day))
            await TimestampsModel.delete_timestamp(marathon_member)

        elif time.time() < timestamp.first_timestamp:
            await message.answer(
                f"Слишком рано. Текстовое сообщение нужно отправить не раньше, чем через "
                f"{seconds_to_time(timestamp.first_timestamp - time.time())}"
            )
    else:
        await message.answer("Таймстемпа нету")




