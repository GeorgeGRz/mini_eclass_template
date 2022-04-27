from django.contrib import admin
from .models import *
from questions.models import Quiz
class FeedFileInline(admin.TabularInline):
    model = CourseFile

class QuizInline(admin.TabularInline):
    model = Quiz


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        FeedFileInline,
        QuizInline,
    ]

admin.site.register(Course, FeedAdmin)