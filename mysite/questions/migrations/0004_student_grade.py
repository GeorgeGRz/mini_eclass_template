# Generated by Django 4.0.3 on 2022-03-28 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_question_points_quiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=200)),
                ('student_surname', models.CharField(max_length=200)),
                ('student_email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField(default=0)),
                ('quiz_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.quiz')),
                ('student_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.student')),
            ],
        ),
    ]
