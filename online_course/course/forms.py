from django.contrib.auth.forms import UserCreationForm
from django import forms
from course.models import Course , Payment
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput




class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','description','duration','price','image','modules']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=PasswordInput)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name','email','phone','whatsapp']
