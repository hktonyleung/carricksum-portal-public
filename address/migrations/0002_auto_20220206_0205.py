# Generated by Django 3.2.9 on 2022-02-06 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='BuildingName',
            new_name='buildingName',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='BuildingNoFrom',
            new_name='buildingNoFrom',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='BuildingNoTo',
            new_name='buildingNoTo',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='District',
            new_name='district',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='FullAddress',
            new_name='fullAddress',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='StreetName',
            new_name='streetName',
        ),
    ]
