# Generated by Django 3.1.8 on 2021-09-25 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0007_timestamps'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PotentialMarathonMembers',
            new_name='FunnelUsers',
        ),
        migrations.AlterField(
            model_name='timestamps',
            name='first_timestamp',
            field=models.PositiveBigIntegerField(verbose_name='Дедлайн первой отметки в милисекундах'),
        ),
        migrations.AlterField(
            model_name='timestamps',
            name='last_timestamp',
            field=models.PositiveBigIntegerField(verbose_name='Дедлайн второй отметки в млмсекундах'),
        ),
        migrations.CreateModel(
            name='OutOfMarathonUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('marathon_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminbot.marathonmembers', verbose_name='Запись в участниках марафона')),
            ],
            options={
                'verbose_name': 'Пользователь, выбывший из марафона',
                'verbose_name_plural': 'Пользователи, выбывшие из марафона',
            },
        ),
    ]