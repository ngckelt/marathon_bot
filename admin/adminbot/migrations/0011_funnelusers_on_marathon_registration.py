# Generated by Django 3.1.8 on 2021-09-30 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0010_funnelusers_last_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='funnelusers',
            name='on_marathon_registration',
            field=models.BooleanField(default=False, verbose_name='Регистрируется на марафон'),
        ),
    ]
