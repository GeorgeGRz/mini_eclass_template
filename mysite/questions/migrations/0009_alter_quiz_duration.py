# Generated by Django 4.0.3 on 2022-04-27 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_quiz_end_time_quiz_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
