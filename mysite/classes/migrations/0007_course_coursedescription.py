# Generated by Django 4.0.3 on 2022-04-05 13:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_remove_course_coursedescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='courseDescription',
            field=ckeditor.fields.RichTextField(default=''),
            preserve_default=False,
        ),
    ]
