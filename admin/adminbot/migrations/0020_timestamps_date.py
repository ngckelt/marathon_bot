# Generated by Django 3.1.8 on 2021-10-02 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0019_remove_timestamps_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamps',
            name='date',
            field=models.CharField(default='asd', max_length=30, verbose_name='Дата'),
            preserve_default=False,
        ),
    ]