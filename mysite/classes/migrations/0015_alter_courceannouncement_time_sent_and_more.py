# Generated by Django 4.0.3 on 2022-05-31 13:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0014_alter_courceannouncement_time_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courceannouncement',
            name='time_sent',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 13, 37, 39, 980400, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='coursefile',
            name='uploaded',
            field=models.DateField(default=datetime.datetime(2022, 5, 31, 13, 37, 39, 980026, tzinfo=utc)),
        ),
    ]
