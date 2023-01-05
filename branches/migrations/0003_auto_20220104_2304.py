# Generated by Django 3.2.9 on 2022-01-04 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branches', '0002_auto_20220104_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='branch_created_by', to='portal.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branch',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branch',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='branch',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]