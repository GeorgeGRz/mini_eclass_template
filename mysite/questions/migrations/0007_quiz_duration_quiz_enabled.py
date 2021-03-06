# Generated by Django 4.0.3 on 2022-04-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_quiz_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='enabled',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
