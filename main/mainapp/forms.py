# certificates/forms.py

from django import forms
from .models import Certificate

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StaffSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ClerkSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CEOSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
class headSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        exclude = ['qr_code','final_certificate']
