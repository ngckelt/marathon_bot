from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Users(TimeBasedModel):
    telegram_id = models.CharField(verbose_name="ID в телеграмме", max_length=30)
    username = models.CharField(verbose_name="Юзернейм в телеграмме", default="Отсутствует", max_length=30)

    def __str__(self):
        if self.username != 'Отсутствует':
            return self.username
        return self.telegram_id

    class Meta:
        abstract = True


class MarathonMembers(Users):
    name = models.CharField(verbose_name="Имя", max_length=255)
    msk_timedelta = models.CharField(verbose_name="Разница с Москвой", max_length=5)
    wakeup_time = models.CharField(verbose_name="Время подъема", max_length=10)
    marathon_day = models.PositiveIntegerField(verbose_name="День марафона", default=0)
    failed_days = models.PositiveIntegerField(verbose_name="Дней пропущено", default=0)
    on_marathon = models.BooleanField(verbose_name="Участвует в марафоне", default=True)

    class Meta:
        verbose_name = "Участник марафона"
        verbose_name_plural = "Участники марафона"


class PotentialMarathonMembers(Users):
    last_message = models.CharField(verbose_name="Последнее сообщение", max_length=255)

    class Meta:
        verbose_name = "Пользователь, который запустил бота"
        verbose_name_plural = "Пользователи, которые запустили бота"


class Moderators(Users):

    class Meta:
        verbose_name = "Модератор"
        verbose_name_plural = "Модераторы"


class Timestamps(TimeBasedModel):
    marathon_member = models.ForeignKey(MarathonMembers, verbose_name="Участник марафона", on_delete=models.CASCADE)
    first_timestamp = models.PositiveIntegerField(verbose_name="Дедлайн первой отметки в милисекундах")
    last_timestamp = models.PositiveIntegerField(verbose_name="Дедлайн второй отметки в млмсекундах")
    first_timestamp_success = models.BooleanField(verbose_name="Статус первой отметки", default=False)
    last_timestamp_success = models.BooleanField(verbose_name="Статус втрой отметки", default=False)

    def __str__(self):
        return self.marathon_member

    class Meta:
        verbose_name = "Временная отметка"
        verbose_name_plural = "Временные отметки"





