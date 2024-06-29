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
        exclude = ['qr_code', 'final_certificate']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'DOB': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Guardian': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Guardian'}),
            'CertificateType': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Certificate Type'}),
            'CadetRank': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Cadet Rank'}),
            'PassingYear': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Passing Year'}),
            'Grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Grade'}),
            'Unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit'}),
            'Directorate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Directorate'}),
            'Place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Place'}),
            'Institute': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Institute'}),
            'certificate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Certificate Number'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Serial Number'}),
            'user_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            # Adjust widget for ImageField as needed, this is a basic example
        }
