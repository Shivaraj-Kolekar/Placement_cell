from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, JobDetail
from .forms import StudentForm, JobDetailForm
from django.core.mail import send_mail

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # Process form data and save to the database
            name = form.cleaned_data['name']
            email=form.cleaned_data['email']
            crn_number = form.cleaned_data['crn_number']
            branch = form.cleaned_data['branch']
            sem_marks_sheet = form.cleaned_data['sem_marks_sheet']
            cv_file = form.cleaned_data['cv_file']

            # Create a new Student instance
            student = Student(
                name=name,
                email=email,
                crn_number=crn_number,
                branch=branch,
                sem_marks_sheet=sem_marks_sheet,
                cv_file=cv_file
            )
            student.save()

            # Send email to user
            subject = "PVG Placement cell registration"
            message = f"Dear {form.cleaned_data['name']}\n\nYou have successfully registered in PVG Placement cell.\n\nThank you!"
            from_email = 'aniketsonkamble07@gmail.com'
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