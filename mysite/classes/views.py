from django.shortcuts import render,get_object_or_404,redirect
from .models import *

from .forms import *
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


def showUsers(request,class_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=class_id)
        return render(request,'classes/users.html',{'course':course})
    else:
        return redirect("/login")