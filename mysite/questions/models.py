from django.db import models
from classes.models import Course
from django.contrib.auth.models import User
from django.utils import timezone
class Quiz(models.Model):
    quiz_title = models.CharField(max_length=200) #title of the quiz
    questions = models.ManyToManyField('Question')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True)
    enabled = models.BooleanField(blank=True,null=True)
    duration = models.IntegerField(blank=True,null=True)
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.quiz_title
    
    @property
    def closed(self) -> bool:
        return timezone.now() < self.end_time

class Question(models.Model):
    exclude = ('user_answer',)
    question_title = models.CharField(max_length=200)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    correct_answer = models.IntegerField()
    choices  = models.ManyToManyField('Choice')
    points = models.FloatField(default=0)

    def __str__(self):
        return self.question_title

class Choice(models.Model):
    
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text
# Create your models here.




class Grade(models.Model):
    student_key = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_key = models.ForeignKey( Quiz,on_delete=models.CASCADE)
    grade = models.FloatField(default = 0)
    def __str__(self):
        return "Grade of " + str(self.student_key)+ " at quiz " + str(self.quiz_key)