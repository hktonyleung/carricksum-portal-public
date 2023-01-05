# Generated by Django 3.2.9 on 2022-03-08 23:03

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_address_uploadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='uploadFile',
            field=models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='address/'),
        ),
    ]
