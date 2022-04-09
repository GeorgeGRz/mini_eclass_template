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
# Create your views here.
def user_register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})