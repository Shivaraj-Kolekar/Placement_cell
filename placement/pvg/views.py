from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
from .models import Student, JobDetail,JobApplication
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentForm, JobDetailForm,StudentLoginForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import get_template
import pandas as pd
import xlsxwriter
import io
from io import BytesIO 
from .helpers import studentlist_pdf,studentlist_xls
from xhtml2pdf import pisa  # Import the module for PDF generation
from django.db.models import Q
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['crn_number'],  # Using email as username
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Create a new Student instance
            student = form.save(commit=False)
            student.user = user  # Assign the user to the student instance
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
        form = StudentForm()

    return render(request, 'signup.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate the user
            student = authenticate(request, username=email, password=password)
            if student is not None:
                # Login the authenticated user
                login(request, student)
                return redirect('student_home')  # Redirect to job list page upon successful login
            else:
                # Handle invalid credentials
                form.add_error(None, "Invalid email or password. Please try again.")
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form})

def my_logout(request):
    logout(request)
    return redirect('student_login')


def admin_home(request):
    return render(request, 'admin_home.html')

def student_home(request):
    return render(request,'student_home.html')

def studentlist(request, page=1):
    search_query = request.GET.get('q')  # Get the search query parameter
    if search_query:  # If there is a search query
        ServiceData = Student.objects.filter(
            Q(crn_number__icontains=search_query) | Q(name__icontains=search_query) | Q(branch__icontains=search_query)
        ).order_by('crn_number')
    else:
        ServiceData = Student.objects.all().order_by('crn_number')


    paginator = Paginator(ServiceData, 10)
    page_number = request.GET.get('page')
    ServiceDataFinal = paginator.get_page(page_number)
    data = {'ServiceData': ServiceDataFinal, 'search_query': search_query}
    return render(request, 'studentlist.html', data)


def delete_std(request, crn_number,page=1):
    s = Student.objects.get(pk=crn_number)
    s.delete()

    return redirect("studentlist",page=page)

def update_std(request, crn_number):
    data = Student.objects.get(pk=crn_number)
    return render(request, "update_std.html", {'data': data})

def do_update_std(request, crn_number, page=1):
    crn_number=request.POST.get("crn_number")
    name=request.POST.get("name")
    email=request.POST.get("email")
    branch=request.POST.get("branch")
    year=request.POST.get("year")
    CGPA=request.POST.get("CGPA")

    data=Student.objects.get(pk=crn_number)

    data.crn_number=crn_number
    data.name=name
    data.email=email
    data.branch=branch
    data.year=year
    data.CGPA=CGPA
    data.save()
    return redirect("studentlist", page=page)
   
# job section
def add_job_details(request):
    if request.method == 'POST':
        form = JobDetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to the database
            form.save()
            return redirect('job_list_admin',page=1)  # Redirect to the home page or any other desired page
        else:
            # Display form errors in case of validation failure
            print(form.errors)
    else:
        form = JobDetailForm()

    return render(request, 'add_job_details.html', {'form': form})



def job_list(request):
    job_details = JobDetail.objects.all()
    return render(request, 'job_list.html', {'job_details': job_details})


def list(request):
    job_details = JobDetail.objects.all()
    return render(request, 'list.html', {'job_details': job_details})
 
@login_required
def apply_for_job(request, job_id):
    if request.method == 'POST':
        job = JobDetail.objects.get(job_id=job_id)
        # Retrieve the Student instance associated with the current user
        student = Student.objects.get(user=request.crn_number
        )
        # Create a job application for the current student and job
        JobApplication.objects.create(student=student, job=job)
        return redirect('job_list')  # Redirect to job list page after applying
    else:
        # Fetch the job details based on the job_id and pass it to the template
        job = JobDetail.objects.get(job_id=job_id)
        return render(request, 'apply_for_job.html', {'job_detail': job})


#Job update and delete section 


def delete_job(request, job_id,page=1):
    s = JobDetail.objects.get(pk=job_id)
    s.delete()

    return redirect("job_list_admin",page=page)

def update_job(request, job_id):
    data = JobDetail.objects.get(pk=job_id)
    return render(request, "update_job.html", {'data': data})

def do_update_job(request, job_id, page=1):
    job_id=request.POST.get("job_id")
    job_title=request.POST.get("job_title")
    company_name=request.POST.get("company_name")
    comany_logo=request.POST.get("company_logo")
    required_branch=request.POST.get("required_branch")
    salary=request.POST.get("salary")
    location=request.POST.get("location")
    CGPA=request.POST.get("CGPA")

    data=JobDetail.objects.get(pk=job_id)

    data.job_id=job_id
    data.job_title=job_title
    data.company_name=company_name
    data.required_branch=required_branch
    data.location=location
    data.CGPA=CGPA
    data.save()
    return redirect("job_list_admin", page=page)
   

def job_list_admin(request, page=1):
    ServiceData = JobDetail.objects.all().order_by('job_id')
    paginator = Paginator(ServiceData, 10)
    page_number = request.GET.get('page')
    ServiceDataFinal = paginator.get_page(page_number)
    data = {'ServiceData': ServiceDataFinal }
    return render(request, 'job_list_admin.html', data)
#  Excel sheet Download
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
# PDF Download
def download_pdf(request):
    queryset = Student.objects.all()
    context = {'ServiceData': queryset}
    pdf = render_to_pdf('studentlist_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=student_data.pdf'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

