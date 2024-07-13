from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

class Student(models.Model):
    crn_number = models.IntegerField(primary_key=True)
    BRANCH_CHOICES = [
        ('ME', 'Mechanical Engineering'),
        ('IT', 'Information Technology'),
        ('CS', 'Computer Science'),
        ('EE', 'Electrical Engineering'),
        ('ENTC', 'ENTC'),
        ('Printing', 'Printing'),
        ('AIDS', 'AIDS')
    ]
    STUDENT_YEAR_CHOICES = [
         ('FE', 'First Year'),
         ('SE', 'Second Year'),
         ('TE', 'Third Year'),
         ('BE', 'Final Year')
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    PLACEMENT_CHOICES = [
        ('On Campus', 'On Campus'),
        ('Off Campus', 'Off Campus')
    ]

    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    year = models.CharField(max_length=20, choices=STUDENT_YEAR_CHOICES)
    passing_year = models.IntegerField(default=0)   
    email = models.EmailField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
     
    CGPA = models.FloatField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    mark_10th = models.FloatField(null=True, blank=True)
    mark_12th = models.FloatField(null=True, blank=True)
    diploma_marks = models.FloatField(null=True, blank=True)
    aggregate_marks = models.FloatField(null=True, blank=True)
    year_down = models.CharField(max_length=5, blank=True)
    active_backlog = models.CharField(max_length=15, blank=True)
    placement_status = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=500, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    placement_type = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default='On Campus')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', null=True, blank=True)

    def calculate_passing_year(self):
        current_year = datetime.now().year
        year_map = {
            'FE': 4,
            'SE': 3,
            'TE': 2,
            'BE': 1
        }
        years_left = year_map.get(self.year, 0)
        passing_year = current_year + years_left
        return passing_year

    def __str__(self):
        return self.name


class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField(max_length=100)
    admin_password = models.CharField(max_length=100)
    admin_branch = models.CharField(max_length=20, choices=Student.BRANCH_CHOICES, default='')

    def __str__(self):
        return self.admin_name


class JobDetail(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    required_passing_year = models.IntegerField(default=2024) 
    salary = models.FloatField(null=True, blank=True)
    required_branchs = models.CharField(max_length=20, choices=Student.BRANCH_CHOICES, default='')
    location = models.CharField(max_length=50, default='')
    system_time = models.DateTimeField()
    required_CGPA = models.FloatField(null=True, blank=True)
    required_marks = models.IntegerField(null=True, blank=True)
    date_exam = models.DateTimeField(default=timezone.now)
    date_last = models.DateTimeField(default=timezone.now)
    venue = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    applied_time = models.DateTimeField(auto_now_add=True)

    ATTENDANCE_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]
    is_present = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES, default='Present')

    def __str__(self):
        return f"{self.student.name} - {self.job.job_id}"
