# forms.py
from django import forms
from .models import Student,JobDetail

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'crn_number', 'branch', 'sem_marks_sheet', 'cv_file']

class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ['job_id','job_title', 'company_logo', 'company_name', 'salary', 'required_branch', 'skills','location']
