from django.contrib import admin
from .models import *

class FeedFileInline(admin.TabularInline):
    model = CourseFile


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        FeedFileInline,
    ]

admin.site.register(Course, FeedAdmin)