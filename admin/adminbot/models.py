from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class MarathonMembers(TimeBasedModel):
    telegram_id = models.CharField(verbose_name="ID в телеграмме", max_length=30)
    username = models.CharField(verbose_name="Юзернейм в телеграмме", default="Отсутствует", max_length=30)
    name = models.CharField(verbose_name="Имя", max_length=255)
    msk_timedelta = models.CharField(verbose_name="Разница с Москвой", max_length=5)
    wakeup_time = models.CharField(verbose_name="Время подъема", max_length=10)
    marathon_day = models.PositiveIntegerField(verbose_name="День марафона", default=0)
    failed_days = models.PositiveIntegerField(verbose_name="Дней пропущено", default=0)
    on_marathon = models.BooleanField(verbose_name="Участвует в марафоне", default=True)

    def __str__(self):
        if self.username != "Отсутствует":
            return self.username
        return self.telegram_id

    class Meta:
        verbose_name = "Участник марафона"
        verbose_name_plural = "Участники марафона"


