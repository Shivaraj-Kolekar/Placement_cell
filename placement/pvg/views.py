from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, JobDetail
from .forms import StudentForm, JobDetailForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import get_template
import pandas as pd
import xlsxwriter
import io
from .helpers import studentlist_pdf,studentlist_xls
from xhtml2pdf import pisa  # Import the module for PDF generation

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to the database
            name = form.cleaned_data['name']
            crn_number = form.cleaned_data['crn_number']
            branch = form.cleaned_data['branch']
            year=form.cleaned_data['year']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            CGPA=form.cleaned_data['CGPA']
          #  sem_marks_sheet = form.cleaned_data['sem_marks_sheet']
          #  cv_file = form.cleaned_data['cv_file']
           
            # Create a new Student instance
            student = Student(
                name=name,
                crn_number=crn_number,
                branch=branch,
                year=year,
           #    sem_marks_sheet=sem_marks_sheet,
           #    cv_file=cv_file,
                email=email,
                password=password,
                CGPA=CGPA
            )
            student.save()

            # Send email to user
            subject = "PVG Placement cell registration"
            message = f"Dear {form.cleaned_data['name']}\n\nYou have successfully registered in PVG Placement cell.\n\nThank you!"
            from_email = 'aniketsonkamble2003@gmail.com'
            recipient_list = [form.cleaned_data['email']]

            send_mail(subject, message, from_email, recipient_list, auth_user='aniketsonkamble07@gmail.com', auth_password='ANUSAYA@0941')

            messages.success(request, 'Registered successfully!')
            return redirect('user_pprofile')
        else:
            # Display form errors in case of validation failure
            print(form.errors)
    else:
        form = StudentForm()

    return render(request, 'signup.html', {'form': form})

def add_job_details(request):
    if request.method == 'POST':
        form = JobDetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to the database
            form.save()
            return redirect('job_list')  # Redirect to the home page or any other desired page
        else:
            # Display form errors in case of validation failure
            print(form.errors)
    else:
        form = JobDetailForm()

    return render(request, 'add_job_details.html', {'form': form})

def login(request):
    return render(request,'login.html')
# @login_required

def job_list(request):
    job_details = JobDetail.objects.all()
    return render(request, 'job_list.html', {'job_details': job_details})


def list(request):
    job_details = JobDetail.objects.all()
    return render(request, 'list.html', {'job_details': job_details})
 
def admin_home(request):
    return render(request, 'admin_home.html')

def update_job_details(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        return redirect('actual_update_job_details', job_id=job_id)

    return render(request, 'update_job_details.html')

def actual_update_job_details(request, job_id):
    job = get_object_or_404(JobDetail, job_id=job_id)  # Assuming 'job_id' is the primary key field

    if request.method == 'POST':
        form = JobDetailForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_details', job_id=job_id)  # Replace 'job_details' with your actual view name
    else:
        form = JobDetailForm(instance=job)

    return render(request, 'actual_update_job_details.html', {'form': form, 'job': job})

def student_home(request):
    return render(request,'student_home.html')

def studentlist(request,page=1):
    ServiceData = Student.objects.all().order_by('crn_number')
    paginator = Paginator(ServiceData, 10)
    page_number = request.GET.get('page')
    ServiceDataFinal = paginator.get_page(page_number)
    data = {'ServiceData': ServiceDataFinal }
    return render(request, 'studentlist.html', data)



def my_view(request, page=1):
    ServiceData = Student.objects.all().order_by('id')
    paginator = Paginator(ServiceData, 10)
    page_number = request.GET.get('page')
    ServiceDataFinal = paginator.get_page(page_number)
    data = {'ServiceData': ServiceDataFinal }
    return render(request, 'my_view.html', data)

def download_excel(request):
    queryset = Student.objects.all()
    context = {'ServiceData': queryset}  # Pass the queryset to the context
    xls_content = studentlist_xls(context)  # Call studentlist_xls with the context
    if xls_content:
        response = HttpResponse(xls_content, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=student_data.xls'
        return response
    else:
        return HttpResponse('Error generating Excel file', status=500)

def download_pdf(request):
    queryset = Student.objects.all()
    context = {'ServiceData': queryset}  # Pass the queryset to the context
    pdf = studentlist_pdf('studentlist.html', context)  # Call studentlist_pdf with the context
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=student_data.pdf'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)