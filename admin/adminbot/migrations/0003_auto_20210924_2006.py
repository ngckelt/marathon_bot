# Generated by Django 3.1.8 on 2021-09-24 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0002_auto_20210924_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marathonmembers',
            name='msk_timedelta',
            field=models.IntegerField(verbose_name='Разница с Москвой'),
        ),
        migrations.CreateModel(
            name='Timestamps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('day', models.PositiveIntegerField(verbose_name='День марафона')),
                ('first_timestamp', models.PositiveBigIntegerField(verbose_name='Время в милисекундах до 1 отметки')),
                ('last_timestamp', models.PositiveBigIntegerField(verbose_name='Время в милисекундах до 2 отметки')),
                ('first_timestamp_success', models.BooleanField(default=False, verbose_name='Успешно прошла 1 отметка')),
                ('last_timestamp_success', models.BooleanField(default=False, verbose_name='Успешно прошла 2 отметка')),
                ('marathon_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminbot.marathonmembers', verbose_name='Участник марафона')),
            ],
            options={
                'verbose_name': 'Отметка о подъеме',
                'verbose_name_plural': 'Отметки о подъемах',
            },
        ),
    ]
