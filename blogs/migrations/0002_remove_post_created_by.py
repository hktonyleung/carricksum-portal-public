# Generated by Django 3.2.9 on 2021-12-03 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created_by',
        ),
    ]
