from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
from .models import Student, JobDetail,JobApplication,Admin
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentForm, JobDetailForm,StudentLoginForm,AdminDetailForm,PlacementForm
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
        form = StudentForm(request.POST)
        if form.is_valid():
            # Create a new user account
            if User.objects.filter(email=form.cleaned_data['email']).exists() or Student.objects.filter(crn_number=form.cleaned_data['crn_number']).exists():
                messages.error(request, 'Email or CRN number already exists.')
                return render(request, 'signup.html', {'form': form})
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']    
                )

                # Additional user profile data can be saved here
                user_profile = form.save(commit=False)
                user_profile.user = user
                user_profile.save()

                # Send email to user
                subject = "PVG Placement cell registration"
                message = f"Dear {form.cleaned_data['name']},\n\nYou have successfully registered in PVG Placement cell.\n\nThank you!"
                from_email = 'aniketsonkamble07@gmail.com'
                recipient_list = [form.cleaned_data['email']]
                try:
                    send_mail(subject, message, from_email, recipient_list, auth_user='aniketsonkamble07@gmail.com', auth_password='pkjllfvwnstdfked')
                except Exception as e:
                    print("An error occurred while sending the email:", e)

                # Log the user in after signing up
                user = authenticate(username=user.username, password=form.cleaned_data['password'])
                login(request, user)
                request.session['crn_number'] = form.cleaned_data['crn_number']
                messages.success(request, 'You have successfully signed up!')
                return redirect('student_home')  # Redirect to the home page or any other desired page
    else:
        form = StudentForm()
    return render(request, 'signup.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Check if the role is Student
        if role == 'Student':
            # Authenticate the student user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # If authenticated, login and redirect to student home page
                login(request, user)
                student = Student.objects.get(email=email)
                crn_number = student.crn_number
                request.session['crn_number'] = crn_number
                return redirect('student_home')
            else:
                # Handle invalid credentials
                error_message = "Invalid email or password. Please try again."
                return render(request, 'student_login.html', {'error_message': error_message})
        elif role == 'Admin':
            # Authenticate the admin user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # If authenticated, login and redirect to admin home page
                login(request, user)
                return redirect('admin_home')
            else:
                # Handle invalid credentials
                error_message = "Invalid email or password for admin. Please try again."
                return render(request, 'student_login.html', {'error_message': error_message})
        else:
            # Handle invalid role
            error_message = "Invalid role. Please select a valid role."
            return render(request, 'student_login.html', {'error_message': error_message})
    else:
        return render(request, 'student_login.html')


def my_logout(request):
    if request.user.is_authenticated:
        # Redirect to the login page
        next_url = '/student_login'  # Or whatever your login page URL is
        response = redirect(next_url)

        # Clear any sensitive session data
        request.session.flush()

        return response

    # If the user is not authenticated, redirect to login page
    return redirect('student_login')

def admin_home(request):
    return render(request, 'admin_home.html')



def add_admin(request):
    form = AdminDetailForm()  # Instantiate the form outside of the conditional block

    if request.method == 'POST':
        form = AdminDetailForm(request.POST, request.FILES)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['admin_email']).exists() or Admin.objects.filter(admin_id=form.cleaned_data['admin_id']).exists():

                messages.error(request, 'Email already exists.')
                return render(request, 'add_admin.html', {'form': form})
            else: 
                user = User.objects.create_user(
                    username=form.cleaned_data['admin_email'],
                    email=form.cleaned_data['admin_email'],
                    password=form.cleaned_data['admin_password']    
                )
                # Save the admin instance
                admin_instance = form.save(commit=False)
                admin_instance.save()
                return redirect('admin_home')  

    return render(request, 'add_admin.html', {'form': form})

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



def delete_std(request, crn_number, page=1):
    student = Student.objects.get(pk=crn_number)
    user = student.user  

    student.delete()

    if user:
        user.delete()

    return redirect("studentlist", page=page)

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
   

def add_job_details(request):
    if request.method == 'POST':
        form = JobDetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to the database
            job = form.save(commit=False)

            # Get the list of selected branches from the form
            selected_branches = request.POST.getlist('required_branchs')
            # Convert the list to a comma-separated string before saving to the database
            job.required_branchs = ', '.join(selected_branches)

            job.save()

            # Retrieve all students
            students = Student.objects.all()

            # Send email to all students
            subject = 'New Job Opening Alert'
            for student in students:
                message = f'Dear {student.name},\n\nA new job opening has been posted: "{job.job_title}". Here are the job details:\n\nJob ID: {job.job_id}\nTitle: {job.job_title}\nCompany Name: {job.company_name}\nSalary: {job.salary}\nLocation: {job.location}\nDate of Exam: {job.date_exam}\nVenue: {job.venue}\n\nThank you for your interest.\n\nFor more details, visit our website:  \n\nBest regards,\nThe PVG Placement Cell'
                from_email = "aniketsonkamble07@gmail.com"
                to_email = student.email
                send_mail(subject, message, from_email, [to_email], fail_silently=False)

            return redirect('job_list_admin', page=1)  # Redirect to the home page or any other desired page
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

def apply_for_job(request, job_id):
    job_detail = JobDetail.objects.get(pk=job_id)
    context = {'job_detail': job_detail, 'job_id': job_id}  # Pass job_id to the context
    return render(request, 'apply_for_job.html', context)


import logging

def apply_for_job2(request, job_id):
    logger = logging.getLogger(__name__)  # Creating a logger instance

    # Retrieve crn_number from the session
    crn_number = request.session.get('crn_number')
    print(crn_number)

    if crn_number is None:
        messages.error(request, 'CRN number is missing from the session.')
        return redirect('job_list')

    try:
        job = JobDetail.objects.get(pk=job_id)
        student = Student.objects.get(crn_number=crn_number)
        
        logger.debug(f"Job: {job}, Student: {student}")  # Add this line for debugging

        existing_application = JobApplication.objects.filter(student=student, job=job).exists()
        
        if existing_application:
            messages.warning(request, 'You have already applied for this job.')
            return redirect('job_list')
        else:
            job_application = JobApplication(student=student, job=job)
            job_application.save()
           
            messages.success(request, 'Successfully applied for the job.')

            # Send notification email
            subject = 'Job Application Confirmation'
            message = f'Dear {student.name},\n\nYou have successfully applied for the job "{job.job_title}". Here are the job details:\n\nJob ID: {job.job_id}\nTitle: {job.job_title}\nCompany Name: {job.company_name}\nSalary: {job.salary}\nLocation: {job.location}\nDate of Exam: {job.date_exam}\nVenue: {job.venue}\n\nThank you for your interest.\n\nBest regards,\nThe PVG Placement Cell'
            from_email = "aniketsonkamble07@gmail.com"
            to_email = [student.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            return redirect('student_home')

    except JobDetail.DoesNotExist:
        messages.error(request, 'Job does not exist.')
        return redirect('job_list')

    except Student.DoesNotExist:
        messages.error(request, 'Student does not exist.')
        return redirect('job_list')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        logger.error(f'An error occurred: {str(e)}')  # Log the error
        return redirect('job_list')

from django.db.models import F  
def applied_jobs(request):
    crn_number = request.session.get('crn_number')  
    print(crn_number)
    if crn_number:
        student = JobApplication.objects.filter(student__crn_number=crn_number)
        job_ids = student.values_list('job_id', flat=True)  # Extract job IDs from student queryset
        job_applications = JobDetail.objects.filter(job_id__in=job_ids)
        job_applications = job_applications.annotate(
            applied_time=F('jobapplication__applied_time')
        )
        print(job_applications)


        return render(request, 'applied_jobs.html', {'job_applications': job_applications})
    else:
        # Redirect or handle case where CRN number is not in session
        return HttpResponse("CRN number not found in session.")

#Job update and delete section 


def delete_job(request, job_id,page=1):
    s = JobDetail.objects.get(pk=job_id)
    s.delete()

    return redirect("job_list_admin",page=page)

def update_job(request, job_id):
    data = JobDetail.objects.get(pk=job_id)
    return render(request, "update_job.html", {'data': data})

def do_update_job(request, job_id, page=1):
    job_title = request.POST.get("job_title")
    company_name = request.POST.get("company_name")
    company_logo = request.FILES.get("company_logo")
    required_branch = request.POST.getlist("required_branch")
    salary = request.POST.get("salary")
    location = request.POST.get("location")
    CGPA = request.POST.get("CGPA")
    required_marks = request.POST.get("required_marks")
    date_exam = request.POST.get("date_exam")
    date_last = request.POST.get("date_last")
    venue = request.POST.get("venue")

    data = JobDetail.objects.get(pk=job_id)
    
    if company_logo:
        data.company_logo = company_logo
    
    data.job_title = job_title
    data.company_name = company_name
    data.required_branch = required_branch
    data.salary = salary
    data.location = location
    data.CGPA = CGPA
    data.required_marks = required_marks
    data.date_exam = date_exam
    data.date_last = date_last
    data.venue = venue
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
    context = {'student': queryset}  
    xls_content = studentlist_xls(context)  
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


def application_list_search(request):
    if request.method == 'GET':
        return render(request, 'application_list_search.html')

def application_list_search_result(request):
    search_applications = request.GET.get('search_applications')
   
    if search_applications:
        # Assuming job_id is an integer field
        try:
            job_id = search_applications
            job_applications = JobApplication.objects.filter(Q(job__job_id=job_id) | Q(job__company_name=search_applications))
            students = [job_app.student for job_app in job_applications]
        except ValueError:
            # Handle cases where the search term is not a valid integer
            students = []
            job_id = ''  # Set job_id to empty string if search term is not valid
    else:
        students = []
        job_id = ''  # Set job_id to empty string if search term is not provided

    context = {
        'students': students,
        'job_id': job_id
    }
    return render(request, 'application_list_search_result.html', context)


from django.shortcuts import get_object_or_404
def download_application_pdf(request,job_id):
    job_application = get_object_or_404(JobApplication, job__job_id=job_id)
    
    students = Student.objects.filter(jobapplication__job__job_id=job_id)
    context = {'students': students}
    pdf = render_to_pdf('application_list_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=student_data.pdf'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)
    
def download_application_excel(request, job_id):
    job_application = get_object_or_404(JobApplication, job__job_id=job_id)
   
    student = Student.objects.filter(jobapplication__job__job_id=job_id)
    context = {'student': student}  

    # Generate Excel content using the custom function
    xls_content = studentlist_xls(context)  

    if xls_content:
        response = HttpResponse(xls_content, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=student_data.xls'
        return response
    else:
        return HttpResponse('Error generating Excel file', status=500)
def placement_list(request):
    placements = Placement.objects.all()
    return render(request, 'placement_list.html', {'placements': placements})

def add_placement(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        form = PlacementForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # Save the form data to the database:
            form.save()
            # Redirect to a success page:
            print("Form saved successfully")  # Debug statement
            return redirect('student_home')  # Replace 'student_home' with the name of your success page URL
        else:
            print("Form is not valid")  # Debug statement
    else:
        # If a GET (or any other method) request, create a blank form:
        crn_number = request.session.get('crn_number')
        form = PlacementForm(initial={'student': crn_number})
    
    # Render the HTML template with the form data:
    print("Rendering the template")  # Debug statement
    return render(request, 'add_placement.html', {'form': form})

