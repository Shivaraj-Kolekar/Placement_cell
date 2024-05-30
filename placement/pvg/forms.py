# forms.py
from django import forms
from .models import Student,JobDetail,Admin

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'crn_number','email','password','name','branch','year','mobile_number','CGPA','mark_10th','mark_12th','diploma_marks','aggregate_marks','year_down','active_backlog','remarks','gender','placement_status','company_name', 'salary',  'placement_type']


class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    ROLES_CHOICES = [('Admin', 'Admin'), ('Student', 'Student')]
    role = forms.ChoiceField(choices=ROLES_CHOICES)

class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ['job_id','job_title', 'company_logo', 'company_name', 'salary', 'required_branchs','location','system_time','required_CGPA','required_marks','date_exam','date_last','venue']


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
    placement_status=forms.CharField(max_length=100, required=False)
    class Meta:
        model = Student
        fields = ['placement_status', 'company_name', 'salary', 'placement_type']
        
class AdminDetailForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['admin_id', 'admin_name', 'admin_email', 'admin_password', 'admin_branch']