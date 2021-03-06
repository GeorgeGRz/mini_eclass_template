from django.shortcuts import render,get_object_or_404,redirect
from datetime import datetime
from django.http import HttpResponse
# Create your views here.
from .models import *
from django.template import loader
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from classes.models import Course
from  .models import Grade
from datetime import datetime,timedelta
from django.utils import timezone

from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        classes = Course.objects.all()
        users_in_zones = Course.objects.filter(enrolledPeople=User.objects.get(pk=request.user.id))
        for x in users_in_zones:
            print(x)
    return render(request,'home.html')


def detail(request,quiz_id):
    if request.user.is_authenticated:
        try:
            quiz = get_object_or_404(Quiz, pk=quiz_id)#get quiz by ID that's sent through url
            
            try:
                grade = Grade.objects.get(quiz_key = quiz, student_key = request.user)
            except Grade.DoesNotExist:
                grade = None
            if grade or timezone.now() > quiz.end_time:
                return redirect("/")
            question = Quiz.objects.get(pk=quiz_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request,'questions/detail.html',{'question': question})
    else:
        return redirect("/")


def results(request,question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def answer(request,question_id):
    
    quiz = get_object_or_404(Quiz, pk=question_id)#get quiz by ID that's sent through url
    
    if timezone.now() > quiz.end_time:
        return redirect("/")
    if  Grade.objects.filter(student_key=request.user,quiz_key=quiz).exists():
        return redirect("/classes")
    
    pts = 0
    print(request.POST)
    choices = []
    for key, value in request.POST.lists():
        if key!='csrfmiddlewaretoken':
            print(key, value)
            selected_choice = quiz.questions.get(pk=key)
            u_choice = UserChoice(question_key=selected_choice,user_choice=int(value[0]))
            u_choice.save()
            choices.append(u_choice)
            if int(value[0]) == selected_choice.correct_answer:
                pts= pts + selected_choice.points
    #First we need to see if user grade exists
    try:
        grade = Grade.objects.get(student_key=request.user,quiz_key=quiz)
        grade.points = pts
        for choice in choices:
            grade.user_choices.add(choice)
        grade.save()
    except Grade.DoesNotExist:
        grd = Grade(student_key=request.user,quiz_key=quiz,grade = pts)
        grd.save()
        for choice in choices:
            print(choice)
            grd.user_choices.add(choice)
        grd.save()
    grd2 = Grade.objects.get(student_key=request.user,quiz_key=quiz)
    return render(request, 'questions/info.html', {"gradeObj": grd})


def create_quiz(request,class_id):
    
    cl = Course.objects.get(pk=class_id)
    print("PRINTING")
    print(cl)
    if not request.user.is_staff:
        raise PermissionDenied()
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuizForm(request.POST)
        qForm = QuestionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = QuizForm()
        qForm = QuestionForm(request.POST)

    return render(request, 'questions/create_quiz.html', {'form': form,'questionForm':qForm,'class':cl})

def submit_new_question(request, class_id):
    print(request.POST)
    qNum = 1
    quiz = Quiz.objects.create(quiz_title=request.POST['quiz_title'],duration=request.POST['duration'])
    course = Course.objects.get(pk=class_id)
    
    for key,value in request.POST.lists():
        if key!='csrfmiddlewaretoken' and key !='quiz_title' and key!='duration':
            print(key,value)
            qt = 'Question '+str(qNum)
            qtext = value[0]
            question_correctChoice = value[1]
            question_points = value[2] 
            question_pub_date = datetime.now()
            question = Question.objects.create(question_title=qt,points = question_points,question_text=qtext,correct_answer=question_correctChoice,pub_date=question_pub_date)
            for v in value[3:]:
                choice = Choice.objects.create(choice_text = v)
                question.choices.add(choice)
            quiz.questions.add(question)
            qNum = qNum + 1
    quiz.course = course
    quiz.save()
    return HttpResponse("You're voting on question %s." % 1)

def quiz_enable(request,class_id,quiz_id):
    #course = Course.objects.get(pk=class_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.start_time = timezone.now()
    quiz.enabled = True
    quiz.end_time = timezone.now() + timedelta(minutes=quiz.duration)
    quiz.save()
    return redirect("/classes/"+str(class_id)+"/quizes")

def quiz_disable(request,class_id,quiz_id):
    #course = Course.objects.get(pk=class_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    
    quiz.enabled = False
    quiz.save()
    return redirect("/classes/"+str(class_id)+"/quizes")


@login_required
def quiz_showAnswered(request,quiz_id):
    grd = Grade.objects.get(student_key=request.user,quiz_key=quiz_id)
    print(grd.user_choices.all())

    return render(request, 'questions/info.html', {"gradeObj": grd})