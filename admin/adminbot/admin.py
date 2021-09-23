from django.contrib import admin
from . import models


@admin.register(models.MarathonMembers)
class MarathonMembersAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'marathon_day', 'failed_days', 'on_marathon']
    search_fields = ['telegram_id', 'username']

    class Meta:
        model = models.MarathonMembers



