# Generated by Django 3.2.9 on 2022-02-20 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('generate_start_date', models.DateTimeField(blank=True, null=True)),
                ('generate_end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('RE', 'READY'), ('GE', 'GENERATING'), ('CO', 'COMPLETED')], default='RE', max_length=2)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
