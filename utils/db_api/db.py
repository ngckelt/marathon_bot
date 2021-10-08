from admin.adminbot.models import *
from asgiref.sync import sync_to_async


def decorate_each_method(decorator):
    def decorate(cls):
        for attr in cls.__bases__[0].__dict__:
            if callable(getattr(cls, attr)) and not attr.startswith('_'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


class MarathonMembersModel:

    @staticmethod
    @sync_to_async
    def add_marathon_member(telegram_id, username, first_name, last_name, phone, msk_timedelta, wakeup_time):
        username = username if username is not None else DEFAULT_USERNAME
        MarathonMembers.objects.create(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            msk_timedelta=msk_timedelta,
            wakeup_time=wakeup_time
        )

    @staticmethod
    @sync_to_async
    def get_marathon_member(telegram_id):
        return MarathonMembers.objects.filter(telegram_id=telegram_id).first()

    @staticmethod
    @sync_to_async
    def get_marathon_member_by_pk(pk):
        return MarathonMembers.objects.filter(pk=pk).first()

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
    def add_funnel_user(telegram_id, username, last_message, last_update_time):
        username = username if username is not None else DEFAULT_USERNAME
        FunnelUsers.objects.create(
            telegram_id=telegram_id,
            username=username,
            last_message=last_message,
            last_update_time=last_update_time
        )

    @staticmethod
    @sync_to_async
    def update_funnel_user(telegram_id, **update_data):
        FunnelUsers.objects.filter(telegram_id=telegram_id).update(**update_data)

    @staticmethod
    @sync_to_async
    def get_funnel_user(telegram_id):
        return FunnelUsers.objects.filter(telegram_id=telegram_id).first()

    @staticmethod
    @sync_to_async
    def get_funnel_users():
        return FunnelUsers.objects.all()

    @staticmethod
    @sync_to_async
    def get_funnel_users_by_filters(**filters):
        return FunnelUsers.objects.filter(**filters)


class OutOfMarathonUsersModel:

    @staticmethod
    @sync_to_async
    def add_out_of_marathon_user(marathon_member):
        OutOfMarathonUsers.objects.create(marathon_member=marathon_member)

    @staticmethod
    @sync_to_async
    def delete_out_of_marathon_user(marathon_member):
        OutOfMarathonUsers.objects.filter(marathon_member=marathon_member).delete()


class TimestampsModel:

    @staticmethod
    @sync_to_async
    def add_timestamp(marathon_member, first_timestamp, last_timestamp, date):
        Timestamps.objects.create(
            marathon_member=marathon_member,
            first_timestamp=first_timestamp,
            last_timestamp=last_timestamp,
            date=date
        )

    @staticmethod
    @sync_to_async
    def get_timestamp(marathon_member, date=None):
        return Timestamps.objects.filter(marathon_member=marathon_member, date=date, completed=False).first()

    @staticmethod
    @sync_to_async
    def get_timestamp_by_pk(timestamp_pk):
        return Timestamps.objects.filter(pk=timestamp_pk).first()

    @staticmethod
    @sync_to_async
    def update_timestamp_by_pk(timestamp_pk, **update_data):
        return Timestamps.objects.filter(pk=timestamp_pk).update(**update_data)

    @staticmethod
    @sync_to_async
    def get_timestamps_by_filters(marathon_member, **filters):
        return Timestamps.objects.filter(**filters)

    @staticmethod
    @sync_to_async
    def update_timestamp(marathon_member, **update_data):
        Timestamps.objects.filter(marathon_member=marathon_member).update(**update_data)

    @staticmethod
    @sync_to_async
    def delete_timestamp(marathon_member):
        Timestamps.objects.filter(marathon_member=marathon_member).delete()


class ReviewsModel:

    @staticmethod
    @sync_to_async
    def get_reviews():
        return Reviews.objects.all()
