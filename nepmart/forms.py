from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
