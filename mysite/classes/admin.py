from django.contrib import admin
from .models import *
from questions.models import Quiz
class FeedFileInline(admin.TabularInline):
    model = CourseFile

class QuizInline(admin.TabularInline):
    model = Quiz

class AnnouncementsInline(admin.TabularInline):
    model = CourceAnnouncement

class FeedAdmin(admin.ModelAdmin):
    inlines = [
        FeedFileInline,
        QuizInline,
        AnnouncementsInline
    ]

admin.site.register(Course, FeedAdmin)

admin.site.register(CourceAnnouncement)