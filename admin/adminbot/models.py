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
        if self.username != "Отсутствует":
            return self.username
        return self.telegram_id

    class Meta:
        abstract = True


class MarathonMembers(Users):
    first_name = models.CharField(verbose_name="Имя", max_length=255, null=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=100, null=True)
    msk_timedelta = models.CharField(verbose_name="Разница с Москвой", max_length=5)
    wakeup_time = models.CharField(verbose_name="Время подъема", max_length=10)
    marathon_day = models.PositiveIntegerField(verbose_name="День марафона", default=0)
    failed_days = models.PositiveIntegerField(verbose_name="Дней пропущено", default=0)
    on_marathon = models.BooleanField(verbose_name="Участвует в марафоне", default=True)

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

    class Meta:
        verbose_name = "Модератор"
        verbose_name_plural = "Модераторы"


class Timestamps(TimeBasedModel):
    marathon_member = models.ForeignKey(MarathonMembers, verbose_name="Участник марафона", on_delete=models.CASCADE)
    first_timestamp = models.PositiveBigIntegerField(verbose_name="Дедлайн первой отметки в милисекундах")
    last_timestamp = models.PositiveBigIntegerField(verbose_name="Дедлайн второй отметки в млмсекундах")
    first_timestamp_success = models.BooleanField(verbose_name="Статус первой отметки", default=False)
    last_timestamp_success = models.BooleanField(verbose_name="Статус втрой отметки", default=False)

    def __str__(self):
        return self.marathon_member.name

    class Meta:
        verbose_name = "Временная отметка"
        verbose_name_plural = "Временные отметки"


class Reviews(TimeBasedModel):
    photo_id = models.CharField(verbose_name="ID фотографии", max_length=255, blank=True)
    video_id = models.CharField(verbose_name="ID видео", max_length=255, blank=True)
    # file = models.FileField(verbose_name="Файл", upload_to='files/', blank=True)

    def __str__(self):
        return f"Отзыв номер {self.pk}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


