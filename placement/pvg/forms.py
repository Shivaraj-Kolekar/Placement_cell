# forms.py
from django import forms
from .models import Student,JobDetail

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'crn_number', 'name',  'branch','email',  'year','password','CGPA']



class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ['job_id','job_title', 'company_logo', 'company_name', 'salary', 'required_branch', 'skills','location','system_time']