from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp

from states.registration.registration import RegisterMarathonMember
from keyboards.inline.wakeup_time_markup import wakeup_time_markup, wakeup_time_callback

from utils.db_api import db


@dp.message_handler(content_types=types.ContentTypes.VIDEO_NOTE)
async def catch_video_note(message: types.Message):
    await message.answer("Сюды попадают видеосообщения")


@dp.message_handler()
async def catch_message(message: types.Message):
    ...




