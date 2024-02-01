from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from .models import Student, JobDetail
from .forms import StudentForm, JobDetailForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Student
from django.core.paginator import Paginator
from django.template.loader import get_template
import pandas as pd
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
            student_class=form.cleaned_data['student_class']
            sem_marks_sheet = form.cleaned_data['sem_marks_sheet']
            cv_file = form.cleaned_data['cv_file']
            email=form.cleaned_data['email']
            # Create a new Student instance
            student = Student(
                name=name,
                crn_number=crn_number,
                branch=branch,
                student_class=student_class,
                sem_marks_sheet=sem_marks_sheet,
                cv_file=cv_file,
                email=email
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
    ServiceData = Student.objects.all().order_by('id')
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
    # Assuming you have a model named Student and you want to export its data
    queryset = Student.objects.all()
    
    # Convert queryset to DataFrame
    df = pd.DataFrame(list(queryset.values()))

    # Convert DataFrame to Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_data.xlsx'
    df.to_excel(response, index=False)

    return response

def download_pdf(request):
    template_path = 'studentlist.html'
    queryset = ServiceData.objects.all()
    context = {'Student': queryset}
    # Render template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=student_data.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF creation error', status=500)