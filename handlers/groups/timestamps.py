import time
from datetime import datetime

from aiogram import types
from loader import dp

from filters.group_chat import GroupOnly
from utils.db_api.db import MarathonMembersModel, TimestampsModel

from utils.timestamps_manage.timestamps_manage import notify_marathon_member_about_success_first_timestamp, \
    update_timestamp, notify_marathon_member_about_fail_first_timestamp, notify_moderator_about_failed_timestamp, \
    update_marathon_member, notify_marathon_member_about_success_last_timestamp, notify_marathon_member_about_fail_day, \
    get_second_timestamp_deadline_time, notify_moderator_about_kick_marathon_member, get_first_timestamp_deadline_time, \
    update_timestamp_by_pk, get_marathon_member_date

from utils.timestamps_manage.utils import MAX_FAILED_DAYS


@dp.message_handler(GroupOnly(), content_types=types.ContentTypes.VIDEO_NOTE)
async def catch_video_note(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is not None:
        timestamp = await TimestampsModel.get_timestamp(marathon_member, get_marathon_member_date(marathon_member))
        if timestamp is not None:
            current_time = time.time()
            # Видеосообщение вовремя
            if timestamp.first_timestamp - current_time > 0:
                if not timestamp.first_timestamp_success:
                    await notify_marathon_member_about_success_first_timestamp(marathon_member)
                    await update_timestamp_by_pk(timestamp.pk, first_timestamp_success=True)
                    message_text = f"Доброе утро! День {marathon_member.marathon_day}/63. " \
                                   f"Чтобы день был засчитан - пришли " \
                                   f"текстовое сообщение, чем полезно было твоё утро, не позднее " \
                                   f"{get_second_timestamp_deadline_time(marathon_member.wakeup_time)}"
                    await message.reply(text=message_text)
            # Опоздал видеосообщение
            elif timestamp.first_timestamp - current_time < 0:
                if not timestamp.first_timestamp_success:
                    # Если это 3й пропуск
                    if marathon_member.failed_days + 1 == MAX_FAILED_DAYS:
                        await message.reply(f"Это действие должно быть выполнено до {marathon_member.wakeup_time}. "
                                            f"Это уже 3й пропуск. Ты обнулился")
                        await notify_moderator_about_kick_marathon_member(marathon_member)
                        await update_marathon_member(marathon_member, failed_days=MAX_FAILED_DAYS, on_marathon=False)
                    else:
                        await message.reply(f"Это действие должно быть выполнено до "
                                            f"{get_first_timestamp_deadline_time(marathon_member.wakeup_time)}. "
                                            f"У вас пропуск. Всего возможно 3 пропуска. Сейчас вы можете дальше "
                                            f"продолжить челленж")
                        await update_marathon_member(marathon_member, failed_days=marathon_member.failed_days + 1)
                        await notify_moderator_about_failed_timestamp(marathon_member)
                    await update_timestamp_by_pk(timestamp.pk, completed=True)


@dp.message_handler(GroupOnly())
async def catch_message(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is not None:
        timestamp = await TimestampsModel.get_timestamp(marathon_member, get_marathon_member_date(marathon_member))
        if timestamp is not None:
            current_time = time.time()
            # Текстовое соощение вовремя
            if timestamp.last_timestamp - current_time > 0:
                if current_time > timestamp.first_timestamp:
                    # Если видеосообщение было прислано вовремя
                    if timestamp.first_timestamp_success:
                        marathon_day = marathon_member.marathon_day + 1
                        await update_marathon_member(marathon_member, marathon_day=marathon_day)
                        await notify_marathon_member_about_success_last_timestamp(marathon_member)
                        await message.reply("День засчитан! Жду тебя завтра ✨")
                        await update_timestamp_by_pk(timestamp.pk, last_timestamp_success=True, completed=True)
                    # Если опоздал с видеосообщением
                    else:
                        await notify_marathon_member_about_fail_day(marathon_member)
                        await notify_moderator_about_failed_timestamp(marathon_member)
                        await update_timestamp_by_pk(timestamp.pk, report_later=True, completed=True)
                        await update_marathon_member(marathon_member, failed_days=marathon_member.failed_days + 1)
                else:
                    ...
                    # await message.reply("Слишком рано")
            else:
                if not timestamp.report_later:
                    await update_timestamp_by_pk(timestamp.pk, report_later=True, completed=True)
                    await notify_moderator_about_failed_timestamp(marathon_member)
                    await notify_marathon_member_about_fail_day(marathon_member)
                    await update_marathon_member(marathon_member, failed_days=marathon_member.failed_days + 1)
                # await message.reply("Опоздал")


