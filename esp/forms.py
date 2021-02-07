from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("first_name", "last_name","username","email",)

class SensorRegForm(forms.ModelForm):
	class Meta:
		model = SensorReg
		fields = '__all__'