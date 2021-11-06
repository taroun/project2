# Generated by Django 3.2.5 on 2021-11-05 13:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animateapp', '0009_auto_20211105_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='animate',
            name='ani1',
            field=models.FileField(blank=True, null=True, upload_to='ani/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['avi', 'mp4', 'mkv', 'mpeg', 'webm'])]),
        ),
        migrations.AddField(
            model_name='animate',
            name='ani2',
            field=models.FileField(blank=True, null=True, upload_to='ani/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['avi', 'mp4', 'mkv', 'mpeg', 'webm'])]),
        ),
        migrations.AddField(
            model_name='animate',
            name='ani3',
            field=models.FileField(blank=True, null=True, upload_to='ani/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['avi', 'mp4', 'mkv', 'mpeg', 'webm'])]),
        ),
    ]