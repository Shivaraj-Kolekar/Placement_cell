from django.db import models

class Student(models.Model):
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
    crn_number = models.CharField(max_length=20)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES,default=''
    )
    student_class=[
         ('FE','First Year'),
         ('SE','Second Year'),
         ('TE','Third Year'),
         ('BE','Final Year')
         ]
    student_class=models.CharField(max_length=20,choices=student_class,default='')
   
    email = models.CharField(max_length=50,default='') 
    sem_marks_sheet = models.FileField(upload_to='sem_marks_sheets/')
    cv_file = models.FileField(upload_to='cv_files/')

    def __str__(self):
        return self.name

class JobDetail(models.Model):
    job_id=models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    required_branch = models.CharField(max_length=50)
    skills = models.TextField()
    location = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.job_title
