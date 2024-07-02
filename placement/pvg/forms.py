from django import forms
from .models import Student, JobDetail, Admin
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = [
            'crn_number', 'email', 'password', 'name', 'branch', 'year',
            'mobile_number', 'CGPA', 'mark_10th', 'mark_12th', 'diploma_marks',
            'aggregate_marks', 'year_down', 'active_backlog', 'remarks',
            'gender', 'placement_status', 'company_name', 'salary', 'placement_type'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return email

    def clean_crn_number(self):
        crn_number = self.cleaned_data.get('crn_number')
        if Student.objects.filter(crn_number=crn_number).exists():
            raise ValidationError('CRN number already exists.')
        return crn_number

class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    ROLES_CHOICES = [('Admin', 'Admin'), ('Student', 'Student')]
    role = forms.ChoiceField(choices=ROLES_CHOICES)

class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ['job_id', 'job_title', 'company_logo', 'company_name', 'salary', 'required_branchs', 'location', 'system_time', 'required_CGPA', 'required_marks', 'date_exam', 'date_last', 'venue']

class PlacementForm(forms.ModelForm):
    ON_CAMPUS = 'On Campus'
    OFF_CAMPUS = 'Off Campus'
    PLACEMENT_CHOICES = [
        (ON_CAMPUS, 'On Campus'),
        (OFF_CAMPUS, 'Off Campus')
    ]
    placement_status = forms.CharField(max_length=100, required=False)
    company_name = forms.CharField(max_length=100, required=False)
    salary = forms.FloatField(required=False)
    placement_type = forms.ChoiceField(choices=PLACEMENT_CHOICES, required=False)

    class Meta:
        model = Student
        fields = ['placement_status', 'company_name', 'salary', 'placement_type']
        
class AdminDetailForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['admin_id', 'admin_name', 'admin_email', 'admin_password', 'admin_branch']

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50)

class SetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']