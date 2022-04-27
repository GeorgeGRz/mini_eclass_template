from django.shortcuts import render,get_object_or_404,redirect,HttpResponse

from questions.models import Quiz, Grade
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

from itertools import chain
# Create your views here.
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
def showUsers(request,class_id):
    course = Course.objects.get(pk=class_id)
    return render(request,'classes/users.html',{'course':course})

@login_required
def files(request,class_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=class_id)
        files = CourseFile.objects.filter(feed=course)
        if not course.enrolledPeople.filter(pk = request.user.pk).exists():
            return redirect("/classes")
        return render(request,'classes/class_files.html',{'course':course,'files':files})
    else:
        return redirect("/login")

@login_required
def list_quizes(request,class_id):
    co = Course.objects.get(pk=class_id)
    if not co.enrolledPeople.filter(pk = request.user.pk).exists():
            return redirect("/classes")
    quizes = Quiz.objects.filter(course=co)
    results = {}
    for quiz in quizes:
        grade = Grade.objects.filter(student_key=request.user,quiz_key=quiz)
        results.setdefault(quiz.quiz_title, grade)

    return render(request,'classes/list_quizes.html',{'course':co,'quizes':results})