from django.forms import ClearableFileInput
from .models import *
from django import forms
class FeedModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['courseName']

class FileModelForm(forms.ModelForm):
    class Meta:
        model = CourseFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
        # widget is important to upload multiple files