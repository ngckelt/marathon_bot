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
    def get_marathon_members_by_filters(**filters):
        return MarathonMembers.objects.filter(**filters)

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

    @staticmethod
    @sync_to_async
    def add_funnel_user(telegram_id, username, last_message):
        FunnelUsers.objects.create(
            telegram_id=telegram_id,
            username=username,
            last_message=last_message
        )

    @staticmethod
    @sync_to_async
    def update_funnel_user(telegram_id, **update_data):
        FunnelUsers.objects.filter(telegram_id=telegram_id).update(**update_data)

    @staticmethod
    @sync_to_async
    def get_funnel_user(telegram_id):
        return FunnelUsers.objects.filter(telegram_id=telegram_id)


class OutOfMarathonUsersModel:

    @staticmethod
    @sync_to_async
    def add_out_of_marathon_user(marathon_member):
        OutOfMarathonUsers.objects.create(marathon_member=marathon_member)

    @staticmethod
    @sync_to_async
    def delete_out_of_marathon_user(marathon_member):
        OutOfMarathonUsers.objects.create(marathon_member=marathon_member)


class TimestampsModel:

    @staticmethod
    @sync_to_async
    def add_timestamp(marathon_member, first_timestamp, last_timestamp):
        Timestamps.objects.create(
            marathon_member=marathon_member,
            first_timestamp=first_timestamp,
            last_timestamp=last_timestamp
        )

    @staticmethod
    @sync_to_async
    def get_timestamp(marathon_member):
        return Timestamps.objects.filter(marathon_member=marathon_member).first()

    @staticmethod
    @sync_to_async
    def update_timestamp(marathon_member, **update_data):
        Timestamps.objects.filter(marathon_member=marathon_member).update(**update_data)

    @staticmethod
    @sync_to_async
    def delete_timestamp(marathon_member):
        Timestamps.objects.filter(marathon_member=marathon_member).delete()

