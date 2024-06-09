from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    CGPA = models.FloatField(null=True, blank=True)  
    mobile_number = models.CharField(max_length=15, blank=True)
    mark_10th = models.FloatField(null=True, blank=True)  
    mark_12th = models.FloatField(null=True, blank=True)  
    diploma_marks = models.FloatField(null=True, blank=True)  
    aggregate_marks = models.FloatField(null=True, blank=True)  
    year_down = models.CharField(max_length=5, blank=True)
    active_backlog = models.CharField(max_length=15, blank=True)
    placement_status=models.CharField(max_length=100,default=None, null=True, blank=True)

    remarks = models.CharField(max_length=500, blank=True)
    gender_select = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = models.CharField(max_length=10, choices=gender_select, blank=True)
    company_name = models.CharField(max_length=100,default=None, null=True, blank=True)
    salary = models.IntegerField(default=None, null=True, blank=True)
   
    ON_CAMPUS = 'On Campus'
    OFF_CAMPUS = 'Off Campus'
    PLACEMENT_CHOICES = [
        (ON_CAMPUS, 'On Campus'),
        (OFF_CAMPUS, 'Off Campus')
    ]
    placement_type = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default=ON_CAMPUS)
    
    # Define a default user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', default=None, null=True, blank=True)

    def __str__(self):
        return self.name



class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    admin_name = models.CharField(max_length=100)
    admin_email = models.CharField(max_length=100)  # Change upload_to to max_length
    admin_password = models.CharField(max_length=100)
    
    BRANCH_CHOICES = [
        ('ME', 'Mechanical Engineering'),
        ('IT', 'Information Technology'),
        ('CS', 'Computer Science'),
        ('EE', 'Electrical Engineering'),
        ('ENTC', 'ENTC'),
        ('Printing', 'Printing'),
        ('AIDS', 'AIDS')
    ]
    admin_branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='')
    
    def __str__(self):
        return self.admin_name  # You can consider returning admin_id or a combination of admin_id and admin_name for better identification


class JobDetail(models.Model):
    job_id = models.IntegerField(primary_key=True)
    job_title = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_name = models.CharField(max_length=100)
    salary = models.FloatField(default=None, null=True, blank=True)
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

    PRESENT = 'Present'
    ABSENT = 'Absent'
    ATTENDANCE_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent')
    ]
    is_present = models.CharField(
        max_length=20,
        choices=ATTENDANCE_CHOICES,
        default=PRESENT  
    )

    def __str__(self):
        return f"{self.student.name} - {self.job.job_id}"

