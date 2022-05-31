from django.shortcuts import render,get_object_or_404,redirect,HttpResponse

from questions.models import Quiz, Grade
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils import timezone
from itertools import chain
from functools import wraps
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


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
        except Course.DoesNotExist:
            raise Http404("Course does not exist")
        return render(request,'classes/detail.html',{'class': course,'files':files})
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
    if not course.enrolledPeople.filter(pk = request.user.pk).exists() and request.user.is_staff == False:
            return redirect("/classes")
    course = Course.objects.get(pk=class_id)
    return render(request,'classes/users.html',{'course':course})

@login_required
def files(request,class_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=class_id)
        files = CourseFile.objects.filter(feed=course)
        if not course.enrolledPeople.filter(pk = request.user.pk).exists() and request.user.is_staff == False:
            return redirect("/classes")
        return render(request,'classes/class_files.html',{'course':course,'files':files})
    else:
        return redirect("/login")

@login_required
def list_quizes(request,class_id):
    co = Course.objects.get(pk=class_id)
    if not co.enrolledPeople.filter(pk = request.user.pk).exists() and request.user.is_staff == False:
            return redirect("/classes")
    quizes = Quiz.objects.filter(course=co) # get all quizes 
    results = {}
    for quiz in quizes:
        grade = Grade.objects.filter(student_key=request.user,quiz_key=quiz)
        results.setdefault(quiz, grade)
    print(results)
    return render(request,'classes/list_quizes.html',{'course':co,'quizes':results,'q':quizes})

from django.core.exceptions import PermissionDenied
@login_required
def file_upload(request,class_id):
    co = Course.objects.get(pk=class_id)
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
            return render(request, 'classes/upload_file.html', {'fileForm':file_form,'class':co})
        else:
            raise PermissionDenied()

@login_required
def chat(request,class_id):
    co = Course.objects.get(pk=class_id)
    return render(request,'classes/live_chat.html',{'class':co})


#handles main page
def mainPage(request):
    courses = Course.objects.all()
    user_courses = []
    lgnForm = AuthenticationForm()
    user_quizes = []
    for crs in courses:
        if crs.enrolledPeople.filter(pk=request.user.id).exists():
            user_courses.append(crs)
            quizes = Quiz.objects.filter(course=crs) 
            for quiz in quizes:
                grade = Grade.objects.filter(student_key=request.user,quiz_key=quiz)
                if grade:
                    user_quizes.append(grade)
    
    
    
    
    
    return render(request,'home.html', {"courses":user_courses,"loginForm":lgnForm,"quizes":user_quizes})


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
        return render(request, 'classes/newAnnouncement.html', {'form':aForm,'class':co})
    