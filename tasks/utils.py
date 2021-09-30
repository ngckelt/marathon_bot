import time
from datetime import timedelta, datetime

MIN_IN_SEC = 60
BASE_SLEEP_SECONDS = 1
FIRST_TIMESTAMP_MINUTES = 10
LAST_TIMESTAMP_MINUTES = 60
MAX_FAILED_DAYS = 3
HALF_AN_HOUR_IN_SEC = 1800
DAY_IN_SEC = 86400


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

