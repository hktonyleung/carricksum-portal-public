# Generated by Django 3.2.9 on 2021-12-03 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0002_room_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='created_by',
        ),
    ]
