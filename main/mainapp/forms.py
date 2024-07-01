# certificates/forms.py

from django import forms
from .models import Certificate
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import StudentDetail, CampDetail

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


from django import forms
from .models import StudentDetail, CampDetail

class CampDetailForm(forms.ModelForm):
    class Meta:
        model = CampDetail
        fields = ['no_name', 'date_month_year', 'location']
        widgets = {
            'no_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No/Name of Camp Attended', 'required': 'true'}),
            'date_month_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Date/Month/Year', 'required': 'true'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location', 'required': 'true'}),
        }

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        fields = ['unit', 'cbse_no', 'rank', 'name', 'dob', 'fathers_name', 'school_college',
                  'year_of_passing_b_certificate', 'attach_photo_b_certificate', 'fresh_or_failure',
                  'attendance_1st_year', 'attendance_2nd_year', 'attendance_3rd_year', 'attendance_total', 'home_address']
        widgets = {
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit', 'required': 'true'}),
            'cbse_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter number or CBSE No', 'required': 'true'}),
            'rank': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter rank', 'required': 'true'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name', 'required': 'true'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select date of birth', 'required': 'true'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter father's name", 'required': 'true'}),
            'school_college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter school or college', 'required': 'true'}),
            'year_of_passing_b_certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter year of passing 'Certificate B'"}),
            'attach_photo_b_certificate': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'fresh_or_failure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter whether fresh or failure', 'required': 'true'}),
            'attendance_1st_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attendance for 1st year', 'required': 'true'}),
            'attendance_2nd_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attendance for 2nd year', 'required': 'true'}),
            'attendance_3rd_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attendance for 3rd year', 'required': 'true'}),
            'attendance_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter total attendance', 'required': 'true'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter home address', 'rows': '3', 'required': 'true'}),
        }
