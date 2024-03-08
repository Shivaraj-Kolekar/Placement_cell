from django.contrib import admin

# Register your models here.
from .models import Student,JobDetail,JobApplication,Admin

admin.site.register(Student),
admin.site.register(JobDetail),
admin.site.register(JobApplication),
admin.site.register(Admin)