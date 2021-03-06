# Generated by Django 3.1.8 on 2021-09-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0011_funnelusers_on_marathon_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('photo_id', models.CharField(max_length=255, null=True, verbose_name='ID фотографии')),
                ('video_id', models.CharField(max_length=255, null=True, verbose_name='ID видео')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
