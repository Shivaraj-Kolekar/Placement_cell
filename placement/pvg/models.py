from django.db import models
from django.utils import timezone

class Student(models.Model):
    crn_number = models.IntegerField(primary_key=True)
    BRANCH_CHOICES = [
        ('ME', 'Mechanical Engineering'),
        ('IT', 'Information Technology'),
        ('CS', 'Computer Science'),
        ('EE', 'Electrical Engineering'),
        ('ENTC', 'ENTC'),
        ('Printing','Printing'),
        ('AIDS','AIDS')
    ]
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    student_year = [
         ('FE','First Year'),
         ('SE','Second Year'),
         ('TE','Third Year'),
         ('BE','Final Year')
    ]
    year = models.CharField(max_length=20, choices=student_year)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    CGPA = models.IntegerField(default=None, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, default='')
    mark_10th = models.IntegerField( default=None, null=True, blank=True)
    mark_12th = models.IntegerField( default=None, null=True, blank=True)
    diploma_marks = models.IntegerField(default=None, null=True, blank=True)
    aggregate_marks = models.IntegerField(default=None, null=True, blank=True)
    year_down = models.CharField(max_length=5, default='')
    active_backlog = models.CharField(max_length=15, default='')
    remarks = models.CharField(max_length=500, default='')
    gender_select = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = models.CharField(max_length=10, choices=gender_select, default='')
   

    def __str__(self):
        return self.name



class JobDetail(models.Model):
    
    job_id = models.IntegerField(primary_key=True)
    job_title = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_name = models.CharField(max_length=100)
    salary = models.IntegerField( default=None, null=True, blank=True)
    BRANCH_CHOICES = [
        ('ME', 'Mechanical Engineering'),
        ('IT', 'Information Technology'),
        ('CS', 'Computer Science'),
        ('EE', 'Electrical Engineering'),
        ('ENTC', 'ENTC'),
        ('Printing', 'Printing'),
        ('AIDS', 'AIDS')
    ]
    required_branchs = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='')
    location = models.CharField(max_length=50, default='')
    system_time = models.DateTimeField()
    required_CGPA = models.IntegerField( default=None, null=True, blank=True)
    required_marks = models.IntegerField(default=None, null=True, blank=True)
    date_exam = models.DateTimeField(default=timezone.now)
    date_last = models.DateTimeField(default=timezone.now)
    venue = models.CharField(max_length=20, default='')
    def __str__(self):
        return self.job_title

class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    applied_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.name} - {self.job.job_id}"