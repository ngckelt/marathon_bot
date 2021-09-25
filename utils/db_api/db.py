from admin.adminbot.models import *
from asgiref.sync import sync_to_async


class MarathonMembersModel:

    @staticmethod
    @sync_to_async
    def add_marathon_member(telegram_id, username, name, msk_timedelta, wakeup_time):
        MarathonMembers.objects.create(
            telegram_id=telegram_id,
            username=username,
            name=name,
            msk_timedelta=msk_timedelta,
            wakeup_time=wakeup_time
        )

    @staticmethod
    @sync_to_async
    def get_marathon_member(telegram_id):
        return MarathonMembers.objects.filter(telegram_id=telegram_id).first()

    @staticmethod
    @sync_to_async
    def get_marathon_members():
        return MarathonMembers.objects.all()

    @staticmethod
    @sync_to_async
    def update_marathon_member(telegram_id, **update_data):
        MarathonMembers.objects.filter(telegram_id=telegram_id).update(**update_data)


class ModeratorsModel:

    @staticmethod
    @sync_to_async
    def get_moderator():
        return Moderators.objects.all().first()


class FunnelUsersModel:
    ...


class TimestampsModel:
    ...

