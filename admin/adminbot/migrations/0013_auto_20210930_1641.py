# Generated by Django 3.1.8 on 2021-09-30 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0012_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='photo_id',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='video_id',
        ),
        migrations.AddField(
            model_name='reviews',
            name='file',
            field=models.FileField(blank=True, upload_to='files/', verbose_name='Файл'),
        ),
    ]
