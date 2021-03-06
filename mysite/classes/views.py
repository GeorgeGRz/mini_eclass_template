from django.shortcuts import render,get_object_or_404,redirect,HttpResponse

from questions.models import Quiz, Grade
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils import timezone
from itertools import chain
from functools import wraps
from django.contrib.auth.forms import AuthenticationForm
import numpy
from django.core import serializers
# Create your views here.

import json

def staff_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            if kwargs['class_id']:
                co = Course.objects.get(pk=kwargs['class_id'])
                if co.professors.filter(pk = request.user.pk).exists():
                    return function(request, *args, **kwargs)
                else:
                    raise PermissionDenied()
            raise PermissionDenied()
    return wrap



def create_to_feed(request):
    user = request.user
    if request.method == 'POST':
        form = FeedModelForm(request.POST)
        file_form = FileModelForm(request.POST, request.FILES)
        print(request.FILES)
        files = request.FILES.getlist('file') #field name in model
        if form.is_valid() and file_form.is_valid():
            feed_instance = form.save(commit=False)
            feed_instance.user = user
            feed_instance.save()
            for f in files:
                file_instance = CourseFile(file=f, feed=feed_instance)
                file_instance.save()

            return redirect("/")
    else:
        form = FeedModelForm()
        file_form = FileModelForm()
    return render(request, 'classes/class_create.html', {'form': form,'fileForm':file_form})

def detail(request,class_id):
    if request.user.is_authenticated:
        try:
            course = Course.objects.get(pk=class_id)
            files = CourseFile.objects.filter(feed=class_id)
            announcements = CourceAnnouncement.objects.filter(course=course).order_by('-time_sent')[:5]
        except Course.DoesNotExist:
            raise Http404("Course does not exist")
        return render(request,'classes/detail.html',{'class': course,'files':files,'announcements':announcements})
    else:
        return redirect("/")

def list_classes(request):
    if request.user.is_authenticated:
        classes = Course.objects.order_by('-courseName')
        return render(request,'classes/list.html',{'courses': classes})
    else:
        return redirect("/")


def user_enroll(request,course_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=course_id)
        if course.enrolledPeople.filter(pk=request.user.id).exists():
            return redirect("/")
        else:
            course.enrolledPeople.add(request.user)
            return redirect("/")
    else:
        return redirect("/login")

@login_required
def user_unregister(request,course_id):
    
    course = Course.objects.get(pk=course_id)
    if not course.enrolledPeople.filter(pk=request.user.id).exists():
        return redirect("/")
    else:
        course.enrolledPeople.remove(request.user)
        course.save()
        return redirect("/")
    

@login_required
def showUsers(request,class_id):
    course = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=course)
    if not course.enrolledPeople.filter(pk = request.user.pk).exists() and request.user.is_staff == False:
            return redirect("/classes")
    course = Course.objects.get(pk=class_id)
    return render(request,'classes/users.html',{'course':course,'announcements':announcements})

@login_required
def files(request,class_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=class_id)
        announcements = CourceAnnouncement.objects.filter(course=course)

        files = CourseFile.objects.filter(feed=course)
        if not course.enrolledPeople.filter(pk = request.user.pk).exists() and request.user.is_staff == False:
            return redirect("/classes")
        return render(request,'classes/class_files.html',{'course':course,'files':files,'announcements':announcements})
    else:
        return redirect("/login")

@login_required
def list_quizes(request,class_id):
    
    co = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=co)
    if not co.enrolledPeople.filter(pk = request.user.pk).exists() and request.user.is_staff == False:
            return redirect("/classes")
    quizes = Quiz.objects.filter(course=co) # get all quizes 
    results = {}
    for quiz in quizes:
        grade = Grade.objects.filter(student_key=request.user,quiz_key=quiz)
        results.setdefault(quiz, grade)
    print(results)
    return render(request,'classes/list_quizes.html',{'course':co,'quizes':results,'q':quizes,'announcements':announcements})

from django.core.exceptions import PermissionDenied
@login_required
def file_upload(request,class_id):
    co = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=co)
    if request.method == 'POST':
        file_form = FileModelForm(request.POST, request.FILES)
        print(request.FILES)
        files = request.FILES.getlist('file') #field name in model
        if file_form.is_valid():
            for f in files:
                print(f)
                file_instance = CourseFile(file=f, feed=co)
                file_instance.save()

            return redirect("/")
    else:
        if request.user.is_staff:
            file_form = FileModelForm()
            return render(request, 'classes/upload_file.html', {'fileForm':file_form,'class':co,'announcements':announcements})
        else:
            raise PermissionDenied()

@login_required
def chat(request,class_id):
    co = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=co)
    return render(request,'classes/live_chat.html',{'class':co,'announcements':announcements})


def sorting_function(announcement):
    return announcement.time_sent

#handles main page
def mainPage(request):
    courses = Course.objects.all()
    user_courses = []
    lgnForm = AuthenticationForm()
    user_quizes = []
    user_announcements = []
    for crs in courses:
        if crs.enrolledPeople.filter(pk=request.user.id).exists():
            user_courses.append(crs)
            announcements = CourceAnnouncement.objects.filter(course=crs).order_by('-time_sent')
            if announcements:
                user_announcements = user_announcements + list(announcements)
                
            quizes = Quiz.objects.filter(course=crs) 
            for quiz in quizes:
                grade = Grade.objects.filter(student_key=request.user,quiz_key=quiz)
                if grade:
                    user_quizes.append(grade)
    #print(user_announcements)
    user_announcements.sort(key=sorting_function,reverse=True)
    #print(user_announcements)
    return render(request,'home.html', {"courses":user_courses,"loginForm":lgnForm,"quizes":user_quizes,'announcements':user_announcements[:5]})


@login_required
@staff_only
def addAnnouncement(request,class_id):
    co = Course.objects.get(pk=class_id)
    if request.method == 'POST':
        anncouncementForm = AnnouncementForm(request.POST)
        if anncouncementForm.is_valid():
            feed_instance = anncouncementForm.save(commit=False)
            feed_instance.course = co
            feed_instance.professor = request.user
            feed_instance.save()
            return redirect("/")
    else:
        aForm = AnnouncementForm()
        announcements = CourceAnnouncement.objects.filter(course=co)
        return render(request, 'classes/newAnnouncement.html', {'form':aForm,'class':co,'announcements':announcements})
    

@login_required
def announcementDetail(request,class_id,announcement_id):
    co = Course.objects.get(pk=class_id)#if user is not enrolled, then redirect him to classes
    if not co.enrolledPeople.filter(pk=request.user.id).exists():
        return redirect("/classes")
    announcement = CourceAnnouncement.objects.get(id=announcement_id)
    print(announcement)
    announcements = CourceAnnouncement.objects.filter(course=co)

    return render(request, 'classes/announcementDetail.html', {'announcement':announcement,'class':co,'announcements':announcements})


@login_required
def classAnnouncements(request,class_id):
    course = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=course)
    
    return render(request,'classes/announcements.html',{'announcements':announcements,'course':course})

@login_required
def userCourseStatistics(request, class_id):
    course = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=course)

    quizes = Quiz.objects.filter(course=course)
    grade_array = numpy.empty(0,float)
    for quiz in quizes:
        
        grades = Grade.objects.filter(quiz_key=quiz, student_key=request.user)
        if grades:
            for gradeObj in grades:
                grade_array = numpy.append(grade_array,gradeObj.grade)
    

    entires_above_5 = len(numpy.where(grade_array >= 5)[0])
    percentage =   entires_above_5  / len(grade_array) * 100
    
    entries_less_5 = len(numpy.where(grade_array<5)[0])
    percentage_less_5 = entries_less_5 / len(grade_array) * 100

    q = {}
    q["avg"] = numpy.average(grade_array)
    q["grades"] = grade_array.tolist()
    q["percentage_over_5"] = percentage
    q["percentage_less_5"] = percentage_less_5
    print(q)
    return render(request,'classes/userStatistics.html',{'announcements':announcements,'class':course,'quizes_stats':q})

@login_required
@staff_only
def courseStatistics(request, class_id):
    course = Course.objects.get(pk=class_id)
    announcements = CourceAnnouncement.objects.filter(course=course)

    quizes = Quiz.objects.filter(course=course)
    quizRet = []
    for quiz in quizes:
        grade_array = numpy.empty(0,float)
        grades = Grade.objects.filter(quiz_key = quiz)
        for gradeObj in grades:
            grade_array = numpy.append(grade_array,gradeObj.grade)

        entires_above_5 = len(numpy.where(grade_array >= 5)[0])
        percentage =   entires_above_5  / len(grade_array) * 100
        
        entries_less_5 = len(numpy.where(grade_array<5)[0])
        percentage_less_5 = entries_less_5 / len(grade_array) * 100
        #print("GRADES: " + str(grade_array))
        #print("AVERAGE IS: " + str(numpy.average(grade_array)))
        #print("PERCENTAGE OF GRADES HIGHER THAN 5: " + str(percentage)+"%")
        #print("90TH percentile: " + str(numpy.percentile(grade_array,90)))
        #print("STANDARD DEVIATION: " + str(numpy.std(grade_array)))
        #print("#SCORES IN RANGE [0-5): " + str( len(numpy.where(numpy.logical_and(grade_array>=0, grade_array< 5))[0])))
        #print("#SCORES IN RANGE [5-10]: " + str( len(numpy.where(numpy.logical_and(grade_array>=5, grade_array<= 10))[0])))
        q = {}
        q["name"] = quiz.quiz_title
        q["grades"] = grade_array.tolist()
        q["avg"] = numpy.average(grade_array)
        q["percentage_over_5"] = percentage
        q["percentage_less_5"] = percentage_less_5
        q["percentile_90"] = numpy.percentile(grade_array,90)
        q["standard_deviation"] = numpy.std(grade_array)
        q["num_scores_0_5"] = len(numpy.where(numpy.logical_and(grade_array>=0, grade_array< 5))[0])
        q["num_scores_5_10"] = len(numpy.where(numpy.logical_and(grade_array>=5, grade_array<= 10))[0])
        quizRet.append(q)
        print("-----")
        
    print(quizRet)
    res = json.dumps( quizRet )
    print(res)
    return render(request,'classes/class_statistics.html',{'announcements':announcements,'class':course,'quizes_stats':res})
