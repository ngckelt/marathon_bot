import aioschedule
from asyncio import sleep

import asyncio
from aiogram.utils.exceptions import ChatNotFound
from utils.db_api.db import MarathonMembersModel, TimestampsModel, \
    ModeratorsModel, OutOfMarathonUsersModel, FunnelUsersModel
from loader import bot
from datetime import datetime

from utils.timestamps_manage.utils import *

from keyboards.inline.moderators import update_marathon_member_statistic_markup
import time

CONTINUE_FUNNEL_AFTER_HALF_AN_HOUR = "👋 Чтобы продолжить наше общение - нажми одну из кнопок. " \
                                     "Возможно ты сейчас занят. Как освободишься, давай продолжим 🤗. " \
                                     "И уже сегодня ты сможешь познакомится с ментором и вступить в чат, " \
                                     "где попробуешь первые 3 дня челленджа! 👍"

CONTINUE_FUNNEL_AFTER_DAY = "Привет! 👋 Мы с тобой вчера не закончили общение. Предлагаю продолжить и познакомится " \
                            "поближе! " \
                            "И уже сегодня ты сможешь познакомится с ментором и вступить в чат, " \
                            "где попробуешь первые 3 дня челленджа! 👍"

CONTINUE_REGISTRATION_AFTER_HALF_AN_HOUR = "Ты так и не ответил 👋. Возможно ты сейчас занят. Я подожду. Как будешь " \
                                           "готов - давай знакомиться! И после этого тебе придёт ссылка на челлендж " \
                                           "и с тобой свяжется ментор"

CONTINUE_REGISTRATION_AFTER_DAY = "Привет! Мы так и не дождались твоего ответа 🙁." \
                                  "Напоминаем о себе. Ты всё ещё хочешь присоединиться к челленджу и попробовать " \
                                  "3 дня в кругу единомышленников вставать в 5-6 утра? " \
                                  "Если да - то давай скорее знакомиться!" \
                                  "Напиши свое Имя и Фамилию 👋."


async def remind_user(funnel_user, message):
    try:
        await bot.send_message(
            chat_id=funnel_user.telegram_id,
            text=message
        )
    except Exception as e:
        print(e, e.__dict__)


async def check_funnel_users():
    current_time = time.time()
    funnel_users = await FunnelUsersModel.get_funnel_users_by_filters(
        on_marathon_registration=False,
        started_marathon=False
    )
    for user in funnel_users:
        # Если прорустил сутки
        if int(current_time - user.last_update_time) in range(DAY_IN_SEC - MIN_IN_SEC // 2, DAY_IN_SEC +
                                                                                            MIN_IN_SEC // 2):
            await remind_user(user, CONTINUE_FUNNEL_AFTER_DAY)

        # Если молчит 30 минут
        elif int(current_time - user.last_update_time) in range(HALF_AN_HOUR_IN_SEC - MIN_IN_SEC // 2,
                                                                HALF_AN_HOUR_IN_SEC + MIN_IN_SEC // 2):
            await remind_user(user, CONTINUE_FUNNEL_AFTER_HALF_AN_HOUR)


async def check_on_registration_funnel_users():
    current_time = time.time()
    funnel_users = await FunnelUsersModel.get_funnel_users_by_filters(
        on_marathon_registration=True,
        started_marathon=False
    )
    for user in funnel_users:
        # Если прорустил сутки
        if int(current_time - user.last_update_time) in range(DAY_IN_SEC - MIN_IN_SEC // 2, DAY_IN_SEC +
                                                                                            MIN_IN_SEC // 2):
            await remind_user(user, CONTINUE_REGISTRATION_AFTER_DAY)

        # Если молчит 30 минут
        elif int(current_time - user.last_update_time) in range(HALF_AN_HOUR_IN_SEC - MIN_IN_SEC // 2,
                                                                HALF_AN_HOUR_IN_SEC + MIN_IN_SEC // 2):
            await remind_user(user, CONTINUE_REGISTRATION_AFTER_HALF_AN_HOUR)
