import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp

from states.registration.registration import RegisterMarathonMember
from keyboards.inline.wakeup_time_markup import wakeup_time_markup, wakeup_time_callback

from utils.db_api import db

from utils.db_api.db import MarathonMembersModel, TimestampsModel


@dp.message_handler(content_types=types.ContentTypes.VIDEO_NOTE)
async def catch_video_note(message: types.Message):
    marathon_member = MarathonMembersModel.get_marathon_member(message.from_user.id)
    timestamp = TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        if timestamp.first_timestamp - time.time() > 0:
            await TimestampsModel.update_timestamp(
                marathon_member=marathon_member,
                first_timestamp_success=True
            )
            await message.answer("Отлично! Видеосообщение засчитано")
    else:
        ...


@dp.message_handler()
async def catch_message(message: types.Message):
    marathon_member = MarathonMembersModel.get_marathon_member(message.from_user.id)
    timestamp = TimestampsModel.get_timestamp(marathon_member)
    if timestamp is not None:
        if timestamp.last_timestamp - time.time() > 0 and timestamp.first_timestamp < time.time():
            await MarathonMembersModel.update_marathon_member(
                telegram_id=marathon_member.telegram_id,
                marathon_day=marathon_member.marathon_day + 1
            )
            await message.answer(f"Ты молодец, задание засчитано, ты уже сделал {marathon_member.marathon_day+1}/60")
            await TimestampsModel.delete_timestamp(marathon_member)
    else:
        ...




