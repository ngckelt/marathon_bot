# Generated by Django 3.1.8 on 2021-09-25 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0006_auto_20210925_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timestamps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('first_timestamp', models.PositiveIntegerField(verbose_name='Дедлайн первой отметки в милисекундах')),
                ('last_timestamp', models.PositiveIntegerField(verbose_name='Дедлайн второй отметки в млмсекундах')),
                ('first_timestamp_success', models.BooleanField(default=False, verbose_name='Статус первой отметки')),
                ('last_timestamp_success', models.BooleanField(default=False, verbose_name='Статус втрой отметки')),
                ('marathon_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminbot.marathonmembers', verbose_name='Участник марафона')),
            ],
            options={
                'verbose_name': 'Временная отметка',
                'verbose_name_plural': 'Временные отметки',
            },
        ),
    ]
