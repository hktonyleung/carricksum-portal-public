# Generated by Django 3.2.9 on 2022-04-06 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_chatroom_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='last_offline_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='last_online_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
