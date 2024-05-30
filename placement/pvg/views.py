from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from .models import Student, JobDetail, JobApplication, Admin
from .forms import StudentForm, JobDetailForm, StudentLoginForm, AdminDetailForm, PlacementForm
from .helpers import studentlist_pdf, studentlist_xls
from xhtml2pdf import pisa
import logging
from io import BytesIO



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
                    password=form.cleaned_data['password'],
                    is_staff=False  # Assuming non-admin users are students
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
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Check user role
                if role == 'Student' and not user.is_staff:
                    login(request, user)
                    return redirect('student_home')
                elif role == 'Admin' and user.is_staff:
                    login(request, user)
                    return redirect('admin_home')
                else:
                    error_message = "Invalid role for the provided credentials."
            else:
                error_message = "Invalid email or password. Please try again."
    else:
        form = StudentLoginForm()
        error_message = None

    return render(request, 'student_login.html', {'form': form, 'error_message': error_message})

def my_logout(request):
    if request.user.is_authenticated:
        # Redirect to the login page
        next_url = '/login'  # Or whatever your login page URL is
        response = redirect(next_url)

        # Clear any sensitive session data
        request.session.flush()

        return response

    # If the user is not authenticated, redirect to login page
    return redirect('student_login')

def admin_home(request):
    total_registrations = Student.objects.count()
    placed_students = Student.objects.filter(placement_status='Placed').count()
    unplaced_students = Student.objects.filter(placement_status='Not Placed').count()

    department_wise_students = []
    branches = ['IT', 'CS', 'ME', 'EE', 'ENTC', 'Printing', 'AIDS']  # Add all your department choices here
    for branch in branches:
        placed_count = Student.objects.filter(branch=branch, placement_status='Placed').count()
        unplaced_count = Student.objects.filter(branch=branch, placement_status='Not Placed').count()
        department_wise_students.append({
            'branch': branch,
            'placed_students': placed_count,
            'unplaced_students': unplaced_count
        })

    context = {
        'total_registrations': total_registrations,
        'placed_students': placed_students,
        'unplaced_students': unplaced_students,
        'department_wise_students': department_wise_students
    }
    return render(request, 'admin_home.html', context)



def add_admin(request):
    form = AdminDetailForm() 

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
    job_details = JobDetail.objects.all()
    return render(request, 'student_home.html', {'job_details': job_details})




def studentlist(request, page=1):
    # Fetch all Student objects from the database
    students = Student.objects.all()

    # Paginate the queryset
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    ServiceData = paginator.get_page(page_number)

    # Pass the paginated queryset to the template context
    context = {'ServiceData': ServiceData}
    return render(request, 'studentlist.html', context)


def delete_std(request, crn_number, page=1):
    try:
        student = Student.objects.get(pk=crn_number)
    except Student.DoesNotExist:
        return HttpResponse("Student not found", status=404)

    # Check if the student has an associated user before trying to delete it
    if hasattr(student, 'user') and student.user is not None:
        student.user.delete()

    # Delete the Student object
    student.delete()

    return redirect("studentlist", page=page)
    

def update_std(request, crn_number):
    data = Student.objects.get(pk=crn_number)
    return render(request, "update_std.html", {'data': data})

def do_update_std(request, crn_number, page=1):
    # Get the student instance
    student_instance = get_object_or_404(Student, pk=crn_number)
    
    # Update the instance with data from the POST request
    student_instance.name = request.POST.get("name")
    student_instance.email = request.POST.get("email")
    student_instance.branch = request.POST.get("branch")
    student_instance.year = request.POST.get("year")
    student_instance.CGPA = request.POST.get("CGPA")
    student_instance.gender = request.POST.get("gender")
    student_instance.mobile_number = request.POST.get("mobile_number")
    student_instance.aggregate_marks = request.POST.get("aggregate_marks")
    student_instance.mark_10th = request.POST.get("mark_10th")
    student_instance.mark_12th = request.POST.get("mark_12th")
    student_instance.diploma_marks = request.POST.get("diploma_marks")
    student_instance.year_down = request.POST.get("year_down")
    student_instance.active_backlog = request.POST.get("active_backlog")
    student_instance.placement_status = request.POST.get("placement_status")
    student_instance.placement_type = request.POST.get("placement_type")
    student_instance.company_name = request.POST.get("company_name")
    
    # Check if salary is empty, then assign default value '00'
    salary = request.POST.get("salary")
    
    # Check if salary is None or empty string, then assign default value '00'
    if salary is None or salary == 'None':
        salary = '00'
    student_instance.salary = salary
    student_instance.save()
 
    return redirect("studentlist", page=page)

def add_job_details(request):
    if request.method == 'POST':
        form = JobDetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to the database
            job = form.save(commit=False)

            # Get the list of selected branches from the form
            selected_branches = request.POST.getlist('required_branchs')
            job.required_branchs = ''.join(selected_branches)
            job.save()
            students = Student.objects.all()
            subject = 'New Job Opening Alert'
            for student in students:
                message = f'Dear {student.name},\n\nA new job opening has been posted: "{job.job_title}". Here are the job details:\n\nJob ID: {job.job_id}\nTitle: {job.job_title}\nCompany Name: {job.company_name}\nSalary: {job.salary}\nLocation: {job.location}\nDate of Exam: {job.date_exam}\nVenue: {job.venue}\n\nThank you for your interest.\n\nFor more details, visit our website:  \n\nBest regards,\nThe PVG Placement Cell'
                from_email = "aniketsonkamble07@gmail.com"
                to_email = student.email
                send_mail(subject, message, from_email, [to_email], fail_silently=False)

            return redirect('job_list_admin', page=1)  
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

def apply_for_job2(request, job_id):
    logger = logging.getLogger(__name__)

    crn_number = request.session.get('crn_number')
    if crn_number is None:
        messages.error(request, 'CRN number is missing from the session.')
        return redirect('student_home')

    try:
        job = JobDetail.objects.get(pk=job_id)
        student = Student.objects.get(crn_number=crn_number)
        
        existing_application = JobApplication.objects.filter(student=student, job=job).exists()
        
        if existing_application:
            messages.error(request, 'You have already applied for this job.')
            return redirect('student_home')

        if student.placement_status == "Placed":
            if student.salary + 2.5 >= job.salary:
                messages.error(request, 'Your salary is not sufficient to apply for this job.')
                return redirect('student_home')
        else:
            if job.required_branchs and student.branch not in job.required_branchs:
                messages.error(request, 'Your branch does not match the required branch for this job.')
                return redirect('student_home')

            if job.required_CGPA and student.CGPA < job.required_CGPA:
                messages.error(request, 'Your CGPA is below the required CGPA for this job.')
                return redirect('student_home')

            if job.required_marks and student.aggregate_marks < job.required_marks:
               messages.error(request, 'Your aggregate marks are below the required aggregate marks for this job.')
               return redirect('student_home')

        job_application = JobApplication(student=student, job=job)
        job_application.save()
        messages.success(request, 'Successfully applied for the job.')

        # Sending email confirmation
        subject = 'Job Application Confirmation'
        message = f'Dear {student.name},\n\nYou have successfully applied for the job "{job.job_title}". Here are the job details:\n\nJob ID: {job.job_id}\nTitle: {job.job_title}\nCompany Name: {job.company_name}\nSalary: {job.salary}\nLocation: {job.location}\nDate of Exam: {job.date_exam}\nVenue: {job.venue}\n\nThank you for your interest.\n\nBest regards,\nThe PVG Placement Cell'
        from_email = "aniketsonkamble07@gmail.com"
        to_email = [student.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)

        return redirect('student_home')
    
    except JobDetail.DoesNotExist:
        messages.error(request, 'Job does not exist.')
    except Student.DoesNotExist:
        messages.error(request, 'Student does not exist.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        logger.error(f'An error occurred: {str(e)}')
    return redirect('student_home')


def applied_jobs(request):
    crn_number = request.session.get('crn_number')  
    if crn_number:
        student = JobApplication.objects.filter(student__crn_number=crn_number)
        job_ids = student.values_list('job_id', flat=True)  
        job_applications = JobDetail.objects.filter(job_id__in=job_ids)
        job_applications = job_applications.annotate(
            applied_time=F('jobapplication__applied_time')
        )

        return render(request, 'applied_jobs.html', {'job_applications': job_applications})
    else:
        return HttpResponse("CRN number not found in session.")


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
    required_branchs = request.POST.getlist("required_branchs")
    salary = request.POST.get("salary")
    location = request.POST.get("location")
    required_CGPA= request.POST.get("required_CGPA")
    required_marks = request.POST.get("required_marks")
    date_exam = request.POST.get("date_exam")
    date_last = request.POST.get("date_last")
    venue = request.POST.get("venue")

    data = JobDetail.objects.get(pk=job_id)
    
    if company_logo:
        data.company_logo = company_logo
    
    data.job_title = job_title
    data.company_name = company_name
    data.required_branchs = required_branchs
    data.salary = salary
    data.location = location
    data.required_CGPA = required_CGPA
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
    students = []
    job_id = ''

    if search_applications:
        try:
            job_id = int(search_applications)
            job_applications = JobApplication.objects.filter(Q(job__job_id=job_id) | Q(job__job_title__icontains=search_applications))
            students = [job_app.student for job_app in job_applications]
        except ValueError:
            # Handle cases where the search term is not a valid integer
            job_applications = JobApplication.objects.filter(job__job_title__icontains=search_applications)
            students = [job_app.student for job_app in job_applications]

    context = {
        'students': students,
        'job_id': job_id
    }
    return render(request, 'application_list_search_result.html', context)


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
    crn_number = request.session.get('crn_number')
    student = Student.objects.get(pk=crn_number)
    
    if request.method == 'POST':
        form = PlacementForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_home')

    else:
        form = PlacementForm(instance=student)
    
    return render(request, 'add_placement.html', {'form': form})