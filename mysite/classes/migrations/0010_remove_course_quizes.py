# Generated by Django 4.0.3 on 2022-04-19 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0009_coursefile_uploaded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='quizes',
        ),
    ]
