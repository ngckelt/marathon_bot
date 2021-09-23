from admin.adminbot.models import *


def add_marathon_member(telegram_id, username, name, msk_timedelta, wakeup_time):
    MarathonMembers.objects.create(
        telegram_id=telegram_id,
        username=username,
        name=name,
        msk_timedelta=msk_timedelta,
        wakeup_time=wakeup_time
    )


