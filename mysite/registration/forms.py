from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField()
	last_name = forms.CharField()
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2","first_name","last_name")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user 