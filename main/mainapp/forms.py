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

# class StudentDetailForm(forms.ModelForm):
#     class Meta:
#         model = StudentDetail
#         fields = ['unit', 'cbse_no', 'rank', 'name', 'dob', 'fathers_name', 'school_college',
#                   'year_of_passing_b_certificate', 'attach_photo_b_certificate', 'fresh_or_failure',
#                   'attendance_1st_year', 'attendance_2nd_year', 'attendance_3rd_year', 'attendance_total', 'home_address']
#         widgets = {
#             'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit', 'required': 'true'}),
#             'cbse_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter number or CBSE No', 'required': 'true'}),
#             'rank': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter rank', 'required': 'true'}),
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name', 'required': 'true'}),
#             'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select date of birth', 'required': 'true'}),
#             'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter father's name", 'required': 'true'}),
#             'school_college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter school or college', 'required': 'true'}),
#             'year_of_passing_b_certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter year of passing 'Certificate B'"}),
#             'attach_photo_b_certificate': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
#             'fresh_or_failure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter whether fresh or failure', 'required': 'true'}),
#             'attendance_1st_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attendance for 1st year', 'required': 'true'}),
#             'attendance_2nd_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attendance for 2nd year', 'required': 'true'}),
#             'attendance_3rd_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attendance for 3rd year', 'required': 'true'}),
#             'attendance_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter total attendance', 'required': 'true'}),
#             'home_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter home address', 'rows': '3', 'required': 'true'}),
#         }

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        exclude = ['marks_subject1', 'marks_subject2', 'marks_subject3']  # Exclude initially

    def clean(self):
        cleaned_data = super().clean()
        fresh_or_failure = cleaned_data.get('fresh_or_failure')

        if fresh_or_failure == 'Pass':
            marks_subject1 = cleaned_data.get('marks_subject1')
            marks_subject2 = cleaned_data.get('marks_subject2')
            marks_subject3 = cleaned_data.get('marks_subject3')

            if not marks_subject1 or not marks_subject2 or not marks_subject3:
                raise forms.ValidationError("Marks for all subjects are required for Pass.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.fresh_or_failure == 'Fail':
            instance.marks_subject1 = None
            instance.marks_subject2 = None
            instance.marks_subject3 = None

        if commit:
            instance.save()
        return instance

class StudentDetailBasicForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        fields = ['unit', 'cbse_no', 'rank', 'name', 'dob', 'fathers_name',
                  'school_college', 'year_of_passing_b_certificate',
                  'attach_photo_b_certificate', 'fresh_or_failure',
                  'attendance_1st_year', 'attendance_2nd_year',
                  'attendance_3rd_year', 'attendance_total', 'home_address']
        

class StudentDetailExtendedForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pass_fail'].widget = forms.Select(choices=[('', '------'), ('Pass', 'Pass'), ('Fail', 'Fail')])
        
        self.fields['marks_subject1'].widget = forms.NumberInput(attrs={'class': 'marks-fields'})
        self.fields['marks_subject2'].widget = forms.NumberInput(attrs={'class': 'marks-fields'})
        self.fields['marks_subject3'].widget = forms.NumberInput(attrs={'class': 'marks-fields'})
        
        if self.instance.pk:
            self.handle_pass_fail(self.instance.pass_fail)
        else:
            self.handle_pass_fail(None)

    def handle_pass_fail(self, pass_fail_value):
        if pass_fail_value == 'Pass':
            self.fields['marks_subject1'].widget.attrs['style'] = 'display:block;'
            self.fields['marks_subject2'].widget.attrs['style'] = 'display:block;'
            self.fields['marks_subject3'].widget.attrs['style'] = 'display:block;'
            self.fields['marks_subject1'].required = True
            self.fields['marks_subject2'].required = True
            self.fields['marks_subject3'].required = True
        else:
            self.fields['marks_subject1'].widget.attrs['style'] = 'display:none;'
            self.fields['marks_subject2'].widget.attrs['style'] = 'display:none;'
            self.fields['marks_subject3'].widget.attrs['style'] = 'display:none;'
            self.fields['marks_subject1'].required = False
            self.fields['marks_subject2'].required = False
            self.fields['marks_subject3'].required = False

    def clean(self):
        cleaned_data = super().clean()
        pass_fail = cleaned_data.get('pass_fail')

        if pass_fail == 'Pass':
            marks_subject1 = cleaned_data.get('marks_subject1')
            marks_subject2 = cleaned_data.get('marks_subject2')
            marks_subject3 = cleaned_data.get('marks_subject3')

            if not marks_subject1 or not marks_subject2 or not marks_subject3:
                raise forms.ValidationError("Marks for all subjects are required for Pass.")
        else:
            cleaned_data['marks_subject1'] = None
            cleaned_data['marks_subject2'] = None
            cleaned_data['marks_subject3'] = None

        return cleaned_data
    
class HelpForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Name', 
            'class': 'form-control form-control-lg thick', 
            'style': 'margin-bottom: 17px;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-mail', 
            'class': 'form-control form-control-lg thick', 
            'style': 'margin-bottom: 17px;'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Message', 
            'class': 'form-control form-control-lg', 
            'rows': 7, 
            'style': 'margin-bottom: 17px;'
        })
    )
    request_type = forms.ChoiceField(
        choices=[('CEO', 'CEO'), ('Staff', 'Staff'), ('Colonel', 'Colonel'),('Cyber3ra Support', 'Cyber3ra Support')],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg thick', 
            'style': 'margin-bottom: 17px;'
        })
    )