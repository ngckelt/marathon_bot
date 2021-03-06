from django.db import models
from data.config import DEFAULT_USERNAME


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Users(TimeBasedModel):
    telegram_id = models.CharField(verbose_name="ID в телеграмме", max_length=30)
    username = models.CharField(verbose_name="Юзернейм в телеграмме", default=DEFAULT_USERNAME, max_length=30)

    def __str__(self):
        if self.username != DEFAULT_USERNAME:
            return self.username
        return self.telegram_id

    class Meta:
        abstract = True


class MarathonMembers(Users):
    first_name = models.CharField(verbose_name="Имя", max_length=255, null=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=100, null=True)
    msk_timedelta = models.IntegerField(verbose_name="Разница с Москвой", default=0)
    wakeup_time = models.CharField(verbose_name="Время подъема", max_length=10)
    marathon_day = models.BigIntegerField(verbose_name="День марафона", default=1)
    failed_days = models.BigIntegerField(verbose_name="Дней пропущено", default=0)
    on_marathon = models.BooleanField(verbose_name="Участвует в марафоне", default=False)

    def __str__(self):
        if self.username != DEFAULT_USERNAME:
            return self.username
        return self.phone

    class Meta:
        verbose_name = "Участник марафона"
        verbose_name_plural = "Участники марафона"


class FunnelUsers(Users):
    last_message = models.CharField(verbose_name="Последнее сообщение", max_length=255)
    started_marathon = models.BooleanField(verbose_name="Начал марафон", default=False)
    last_update_time = models.PositiveIntegerField(verbose_name="Время последнего сообщения", default=0)
    on_marathon_registration = models.BooleanField(verbose_name="Регистрируется на марафон", default=False)

    class Meta:
        verbose_name = "Пользователь, который запустил бота"
        verbose_name_plural = "Пользователи, которые запустили бота"


class OutOfMarathonUsers(TimeBasedModel):
    marathon_member = models.ForeignKey(MarathonMembers, verbose_name="Запись в участниках марафона",
                                        on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        MarathonMembers.objects.filter(telegram_id=self.marathon_member.telegram_id).update(
            on_marathon=True,
            failed_days=0
        )
        super(OutOfMarathonUsers, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь, выбывший из марафона"
        verbose_name_plural = "Пользователи, выбывшие из марафона"


class Moderators(Users):
    name = models.CharField(verbose_name="Имя", max_length=255)

    class Meta:
        verbose_name = "Модератор"
        verbose_name_plural = "Модераторы"


class Timestamps(TimeBasedModel):
    marathon_member = models.ForeignKey(MarathonMembers, verbose_name="Участник марафона", on_delete=models.CASCADE)
    first_timestamp = models.PositiveBigIntegerField(verbose_name="Дедлайн первой отметки в секундах")
    last_timestamp = models.PositiveBigIntegerField(verbose_name="Дедлайн второй отметки в секундах")
    first_timestamp_success = models.BooleanField(verbose_name="Вовремя сдан первый отчет", default=False)
    last_timestamp_success = models.BooleanField(verbose_name="Вовремя сдан второй отчет", default=False)
    report_later = models.BooleanField(verbose_name="Отправил отчеты, но с опозданием", default=False)
    date = models.CharField(verbose_name="Дата", max_length=30)
    completed = models.BooleanField(verbose_name="Завершено", default=False)

    def __str__(self):
        return self.marathon_member.first_name

    class Meta:
        verbose_name = "Временная отметка"
        verbose_name_plural = "Временные отметки"


class Reviews(TimeBasedModel):
    photo_id = models.CharField(verbose_name="ID фотографии", max_length=255, blank=True)
    video_id = models.CharField(verbose_name="ID видео", max_length=255, blank=True)

    def __str__(self):
        return f"Отзыв номер {self.pk}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


