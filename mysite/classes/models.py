from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from questions.models import Quiz
import os
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

import math
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

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
    uploaded = models.DateField(default=datetime.date.today)
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    def name(self):
        filename =  os.path.basename(self.file.name)
        return filename
    def size(self):
        return convert_size(self.file.size)
    