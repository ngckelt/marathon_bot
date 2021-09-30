from django.contrib import admin
from . import models


@admin.register(models.MarathonMembers)
class MarathonMembersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'username', 'wakeup_time', 'marathon_day', 'failed_days', 'on_marathon']
    search_fields = ['telegram_id', 'username']

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
    list_display = ['marathon_member', 'first_timestamp_success', 'last_timestamp_success']

    class Meta:
        model = models.Timestamps


@admin.register(models.OutOfMarathonUsers)
class OutOfMarathonUsersAdmin(admin.ModelAdmin):
    list_display = ['marathon_member']

    class Meta:
        model = models.OutOfMarathonUsers
