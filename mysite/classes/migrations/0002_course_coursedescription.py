# Generated by Django 4.0.3 on 2022-04-05 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='courseDescription',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
