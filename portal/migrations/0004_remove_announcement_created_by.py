# Generated by Django 3.2.9 on 2021-12-03 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_announcement_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='created_by',
        ),
    ]