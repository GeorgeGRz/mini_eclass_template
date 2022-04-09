from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from questions.models import Quiz
import os
from ckeditor_uploader.fields import RichTextUploadingField

class Course(models.Model):
    enrolledPeople  = models.ManyToManyField(User)
    courseDescription = RichTextUploadingField()
    courseName=models.CharField(blank=False, max_length=500)
    quizes = models.ManyToManyField(Quiz,blank=True)
    professors = models.ManyToManyField(User, limit_choices_to={'groups__name': "Staff"},related_name="teachers")

    def __str__(self):
        return self.courseName

class CourseFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    feed = models.ForeignKey(Course, on_delete=models.CASCADE)
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    
