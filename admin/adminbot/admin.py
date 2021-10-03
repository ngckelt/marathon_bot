from django.contrib import admin
from . import models


@admin.register(models.MarathonMembers)
class MarathonMembersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'username', 'wakeup_time', 'marathon_day', 'failed_days', 'on_marathon']
    search_fields = ['telegram_id', 'username', 'phone']
    list_filter = ['on_marathon']

    class Meta:
        model = models.MarathonMembers


@admin.register(models.FunnelUsers)
class FunnelUsersAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'last_message']

    class Meta:
        models = models.FunnelUsers


@admin.register(models.Moderators)
class ModeratorsAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username']

    class Meta:
        model = models.Moderators


@admin.register(models.Timestamps)
class TimestampsAdmin(admin.ModelAdmin):
    list_display = ['marathon_member', 'first_timestamp_success',
                    'last_timestamp_success', 'report_later', 'completed', 'date']
    search_fields = ['marathon_member__phone', 'marathon_member__username', 'date']
    list_filter = ['completed']

    class Meta:
        model = models.Timestamps


@admin.register(models.OutOfMarathonUsers)
class OutOfMarathonUsersAdmin(admin.ModelAdmin):
    list_display = ['marathon_member']
    search_fields = ['marathon_member__phone', 'marathon_member__username']

    class Meta:
        model = models.OutOfMarathonUsers


@admin.register(models.Reviews)
class ReviewsAdmin(admin.ModelAdmin):

    class Meta:
        model = models.Reviews


