from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

import os
from ckeditor_uploader.fields import RichTextUploadingField
import datetime
from django.utils import timezone

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
    
    professors = models.ManyToManyField(User, limit_choices_to={'is_staff': True},related_name="teachers")

    def __str__(self):
        return self.courseName

class CourseFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    feed = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded = models.DateField(default=timezone.datetime.now)
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    def name(self):
        filename =  os.path.basename(self.file.name)
        return filename
    def size(self):
        return convert_size(self.file.size)
    
class CourceAnnouncement(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    time_sent = models.DateTimeField(default=timezone.datetime.now)
    title = models.CharField(max_length=60)
    body = RichTextUploadingField()
    professor = models.ForeignKey(User, limit_choices_to={'is_staff': True},related_name="professor",on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title + " " + str(self.time_sent)