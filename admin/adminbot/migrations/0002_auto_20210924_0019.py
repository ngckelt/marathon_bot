# Generated by Django 3.1.8 on 2021-09-23 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marathonmembers',
            old_name='msk',
            new_name='msk_timedelta',
        ),
        migrations.AlterField(
            model_name='marathonmembers',
            name='username',
            field=models.CharField(default='Отсутствует', max_length=30, verbose_name='Юзернейм в телеграмме'),
        ),
    ]
