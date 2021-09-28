import time
from datetime import timedelta, datetime

MIN_IN_SEC = 60


def format_time(str_time: str) -> str:
    if str_time.startswith('0'):
        str_time = str_time.replace('0', '', 1)
    return str_time


def times_equal(now: datetime, user_time: str, msk_timedelta: int) -> bool:
    delta = timedelta(hours=msk_timedelta)
    time_with_delta = now + delta
    return format_time(time_with_delta.strftime("%H-%M")) == format_time(user_time)


def set_timestamp(minutes: int) -> int:
    return int(time.time()) + (MIN_IN_SEC * minutes)

