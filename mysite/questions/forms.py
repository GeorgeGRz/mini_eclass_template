from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class QuizForm(forms.Form):
    class Meta:
        model = Quiz
        fields = ['quiz_title']
    quiz_title = forms.CharField(max_length=100)


class QuestionForm(forms.Form):
    class Meta:
        model = Question
        fields = ['question_title','question_text','choices']
    question_title = forms.CharField(max_length=100)
    question_text = forms.CharField(max_length=100)
    choices = forms.ModelMultipleChoiceField(
        queryset=Choice.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

