import time
from datetime import datetime, timedelta

from data.config import DEFAULT_USERNAME

MIN_IN_SEC = 60
FIRST_TIMESTAMP_MINUTES = 130
LAST_TIMESTAMP_MINUTES = 210
MAX_FAILED_DAYS = 3
HALF_AN_HOUR_IN_SEC = 1800
DAY_IN_SEC = 86400
SUCCESS_FIRST_TIMESTAMP_MESSAGE_INDEX = 0
SUCCESS_LAST_TIMESTAMP_MESSAGE_INDEX = 1
HOUR_AND_HALF_IN_SEC = 5400


def format_time(str_time: str) -> str:
    while str_time.startswith('0'):
        str_time = str_time.replace('0', '', 1)
    return str_time


def times_equal(now: datetime, user_time: str, msk_timedelta: int) -> bool:
    delta = timedelta(hours=msk_timedelta+2)
    time_with_delta = now + delta
    return format_time(time_with_delta.strftime("%H-%M")) == format_time(user_time)


def set_timestamp(minutes: int) -> int:
    return int(time.time()) + (MIN_IN_SEC * minutes)


def get_second_timestamp_deadline_time(time: str) -> str:
    return {
        '5-00': '6:30',
        '5-30': '7:00',
        '6-00': '7:30',
    }.get(time)


def get_first_timestamp_deadline_time(time: str) -> str:
    return {
        '5-00': '6:10',
        '5-30': '5:40',
        '6-00': '6:10',
    }.get(time)


def get_marathon_member_contact(marathon_member):
    contacts = f"{marathon_member.first_name} {marathon_member.last_name} "
    if marathon_member.username != DEFAULT_USERNAME:
        contacts += f"@{marathon_member.username}"
    else:
        contacts += f"{marathon_member.phone}"
    return contacts


def get_marathon_member_date(marathon_member):
    now = datetime.now()
    delta = timedelta(hours=marathon_member.msk_timedelta+2)
    time_with_delta = now + delta
    return time_with_delta.strftime("%d.%m.%Y")


