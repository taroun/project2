# Generated by Django 3.2.5 on 2021-11-03 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animateapp', '0004_auto_20211103_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animate',
            name='ani',
            field=models.FileField(null=True, upload_to='ani/'),
        ),
    ]
