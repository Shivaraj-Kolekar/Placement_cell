from django.db import models

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
    sem_marks_sheet = models.FileField(upload_to='sem_marks_sheets/')
    cv_file = models.FileField(upload_to='cv_files/')
    CGPA = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name



class JobDetail(models.Model):
    
    job_id =models.IntegerField(primary_key=True)
    job_title = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    required_branch = models.CharField(max_length=50)
    skills = models.TextField()
    location = models.CharField(max_length=50, default='')
    system_time=models.DateTimeField()
    def __str__(self):
        return self.job_title

class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    applied_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student.name} - {self.job.job_title}"