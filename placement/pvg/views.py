from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView  # Import View and TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from .models import Student, JobDetail, JobApplication, Admin
from .forms import StudentForm, JobDetailForm, StudentLoginForm, AdminDetailForm, PlacementForm, PasswordResetForm,SetPasswordForm
from .helpers import studentlist_pdf, studentlist_xls
from xhtml2pdf import pisa
import logging
from django.urls import reverse
from django.utils import timezone

from io import BytesIO
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy
import plotly.graph_objs as go
import plotly.offline as py

def index(request):
    return render(request, 'index.html')

def a(request):
    return render(request,'a.html')

def signup(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Create user object
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                is_staff=False
            )

            # Save student profile with passing year
            user_profile = form.save(commit=False)
            user_profile.user = user
            user_profile.passing_year = user_profile.calculate_passing_year()  # Calculate passing year
            user_profile.save()

            # Send registration email
            subject = "PVG Placement cell registration"
            message = f"Dear {form.cleaned_data['name']},\n\nYou have successfully registered in PVG Placement cell.\n\nThank you!"
            from_email = 'your-email@example.com'  # Update with your actual email
            recipient_list = [form.cleaned_data['email']]
            send_mail(subject, message, from_email, recipient_list)

            # Log in the user after signing up
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                request.session['crn_number'] = form.cleaned_data['crn_number']
                messages.success(request, 'You have successfully signed up!')
                return redirect('student_home')
            else:
                messages.error(request, 'Authentication failed. Please try logging in.')
        else:
            # Handle form errors gracefully
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

            # Re-render the form with errors and data
            return render(request, 'signup.html', {'form': form})
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
                    try:
                        student = Student.objects.get(user=user)
                        crn_number = student.crn_number
                        login(request, user)
                        request.session['crn_number'] = crn_number
                        messages.success(request, "Login successful. Welcome, student!")
                        return redirect('student_home')
                    except Student.DoesNotExist:
                        messages.error(request, "Student profile not found.")
                        return redirect('student_login')
                elif role == 'Admin' and user.is_staff:
                    login(request, user)
                    messages.success(request, "Login successful. Welcome, admin!")
                    return redirect('admin_home')
                else:
                    messages.error(request, "Invalid role for the provided credentials.")
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Form data is not valid. Please correct the errors below.")
    else:
        form = StudentLoginForm()

    return render(request, 'student_login.html', {'form': form})


def my_logout(request):
    if request.user.is_authenticated:
        # Log out the user
        logout(request)

        # Prevent caching of pages after logout
        response = redirect('student_login')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1
        response['Pragma'] = 'no-cache'  # HTTP 1.0
        response['Expires'] = '0'  # Proxies
        return response

    # If the user is not authenticated, redirect to login page
    return redirect('student_login')

User = get_user_model()

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,  # Change to your domain
                        'site_name': 'PVG Placement Cell',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'from@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect("student_login")
            else:
                messages.error(request, 'No user is associated with this email address.')
                return redirect("password_reset")
    else:
        form = PasswordResetForm()
    return render(request, "password_reset.html", {"form": form})

class PasswordResetConfirmViewCustom(View):
    def get(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs['uidb64']
            token = kwargs['token']
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['reset_user_id'] = user.id  # Store user id in session for security

            # Proceed with password reset form
            form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})

        messages.error(request, 'The reset link is no longer valid.')
        return redirect('password_reset')

    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You may now log in.')
                return redirect('student_login')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            messages.error(request, 'The reset link is no longer valid.')

        return render(request, 'password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})

class PasswordResetCompleteRedirectView(TemplateView):
    template_name = 'student_login.html'  

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Password reset is complete. You may now log in.')
        return redirect(reverse_lazy('student_login'))



def profile(request):
    crn_number = request.session.get('crn_number')
    if not crn_number:
        # Handle the case where the CRN number is not found in the session
        return redirect('student_home')  # Redirect to an error page or handle appropriately

    student = get_object_or_404(Student, crn_number=crn_number)
    return render(request, 'profile.html', {'student': student})



def admin_home(request):
    year = request.GET.get('year', None)  # Get the year parameter from the request

    # Filter students based on the year parameter if provided
    if year:
        total_registrations = Student.objects.filter(passing_year=year).count()
        placed_students = Student.objects.filter(passing_year=year, placement_status='Placed').count()
        unplaced_students = Student.objects.filter(passing_year=year, placement_status='Not Placed').count()

        department_wise_students = []
        branches = ['IT', 'CS', 'ME', 'EE', 'ENTC', 'Printing', 'AIDS']  # Add all your department choices here
        for branch in branches:
            placed_count = Student.objects.filter(passing_year=year, branch=branch, placement_status='Placed').count()
            unplaced_count = Student.objects.filter(passing_year=year, branch=branch, placement_status='Not Placed').count()
            department_wise_students.append({
                'branch': branch,
                'placed_students': placed_count,
                'unplaced_students': unplaced_count
            })
    else:
        # If no year parameter is provided, show all data (default behavior)
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
        'department_wise_students': department_wise_students,
        'selected_year': year  # Pass the selected year to the template for display purposes
    }
    return render(request, 'admin_home.html', context)



def download_student_data(request, branch, status, year):
    # Prepare filter conditions based on branch, status, and year
    if year and year != '0':
        queryset = Student.objects.filter(branch=branch, placement_status=status, passing_year=year)
    else:
        queryset = Student.objects.filter(branch=branch, placement_status=status)

    # Generate Excel content
    xls_content = studentlist_xls({'student': queryset})

    if xls_content:
        filename = f'student_data_{branch}_{status}'
        if year and year != '0':
            filename += f'_{year}'
        filename += '.xls'

        response = HttpResponse(xls_content, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse('Error generating Excel file', status=500)




def graphical_representation(request):
    years = Student.objects.values_list('passing_year', flat=True).distinct().order_by('passing_year')
    branches = ['IT', 'CS', 'ME', 'EE', 'ENTC', 'Printing', 'AIDS']  # List of department choices

    selected_year = request.GET.get('year', None)
    selected_graph_type = request.GET.get('graph_type', 'bar')  # Default to bar chart if not specified

    if selected_year:
        department_wise_data = []
        for branch in branches:
            placed_count = Student.objects.filter(passing_year=selected_year, branch=branch, placement_status='Placed').count()
            unplaced_count = Student.objects.filter(passing_year=selected_year, branch=branch, placement_status='Not Placed').count()
            department_wise_data.append({
                'branch': branch,
                'placed_students': placed_count,
                'unplaced_students': unplaced_count
            })

        if selected_graph_type == 'bar':
            graph_data = create_bar_chart(department_wise_data)
        elif selected_graph_type == 'line':
            graph_data = create_line_chart(department_wise_data)
        elif selected_graph_type == 'pie':
            graph_data = create_pie_chart(department_wise_data)
        elif selected_graph_type == 'area':
            graph_data = create_area_chart(department_wise_data)
        else:
            graph_data = create_bar_chart(department_wise_data)  # Default to bar chart

        context = {
            'years': years,
            'branches': branches,
            'selected_year': selected_year,
            'selected_graph_type': selected_graph_type,
            'graph_data': graph_data
        }
    else:
        # If no year is selected, show aggregate data for landing page
        aggregate_data = get_aggregate_data()
        graph_data = create_pie_chart_aggregate(aggregate_data)

        context = {
            'years': years,
            'branches': branches,
            'selected_year': selected_year,
            'selected_graph_type': 'pie',  # Default to pie chart for landing page
            'graph_data': graph_data
        }

    return render(request, 'graphical_representation.html', context)

def get_aggregate_data():
    # Function to get aggregate data (total placed vs. unplaced students across all years and branches)
    aggregate_data = {
        'placed': Student.objects.filter(placement_status='Placed').count(),
        'unplaced': Student.objects.filter(placement_status='Not Placed').count()
    }
    return aggregate_data

def create_pie_chart_aggregate(data):
    # Create a pie chart for aggregate data using Plotly
    labels = ['Placed', 'Not Placed']
    values = [data['placed'], data['unplaced']]

    trace = go.Pie(labels=labels, values=values, hole=0.3)

    layout = go.Layout(title='Aggregate Placement Status')

    fig = go.Figure(data=[trace], layout=layout)
    graph_div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return graph_div

def create_bar_chart(data):
    x_values = [item['branch'] for item in data]
    placed_values = [item['placed_students'] for item in data]
    unplaced_values = [item['unplaced_students'] for item in data]

    trace1 = go.Bar(x=x_values, y=placed_values, name='Placed', marker=dict(color='blue'))
    trace2 = go.Bar(x=x_values, y=unplaced_values, name='Not Placed', marker=dict(color='red'))

    layout = go.Layout(title='Branch-wise Placement Status',
                       xaxis=dict(title='Branch'),
                       yaxis=dict(title='Number of Students'),
                       barmode='stack')

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    graph_div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return graph_div

def create_line_chart(data):
    x_values = [item['branch'] for item in data]
    placed_values = [item['placed_students'] for item in data]
    unplaced_values = [item['unplaced_students'] for item in data]

    trace1 = go.Scatter(x=x_values, y=placed_values, mode='lines+markers', name='Placed', line=dict(color='green'))
    trace2 = go.Scatter(x=x_values, y=unplaced_values, mode='lines+markers', name='Not Placed', line=dict(color='orange'))

    layout = go.Layout(title='Branch-wise Placement Trends',
                       xaxis=dict(title='Branch'),
                       yaxis=dict(title='Number of Students'))

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    graph_div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return graph_div

def create_pie_chart(data):
    labels = [item['branch'] for item in data]
    values_placed = [item['placed_students'] for item in data]
    values_unplaced = [item['unplaced_students'] for item in data]
    total_students = [values_placed[i] + values_unplaced[i] for i in range(len(data))]

    trace1 = go.Pie(labels=labels, values=values_placed, name='Placed', hole=0.3, 
                    marker=dict(colors=['#7CB342', '#4CAF50', '#CDDC39']),
                    hoverinfo='label+percent',
                    textinfo='value+label',
                    textposition='inside',
                    insidetextorientation='radial',
                    text=[f'Placed: {v}/{total_students[i]}' for i, v in enumerate(values_placed)])

    trace2 = go.Pie(labels=labels, values=values_unplaced, name='Not Placed', hole=0.3, 
                    marker=dict(colors=['#FF7043', '#FFA726', '#FFCC80']),
                    hoverinfo='label+percent',
                    textinfo='value+label',
                    textposition='inside',
                    insidetextorientation='radial',
                    text=[f'Not Placed: {v}/{total_students[i]}' for i, v in enumerate(values_unplaced)])

    layout = go.Layout(title='Distribution of Placed and Unplaced Students by Branch',
                       legend=dict(orientation='h', x=0.5, y=-0.1),
                       margin=dict(l=20, r=20, t=60, b=20))

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    graph_div = py.plot(fig, output_type='div', include_plotlyjs=False)

    return graph_div


def create_area_chart(data):
    x_values = [item['branch'] for item in data]
    placed_values = [item['placed_students'] for item in data]
    unplaced_values = [item['unplaced_students'] for item in data]

    trace1 = go.Scatter(x=x_values, y=placed_values, mode='lines', fill='tozeroy', name='Placed', fillcolor='rgba(152, 251, 152, 0.5)')
    trace2 = go.Scatter(x=x_values, y=unplaced_values, mode='lines', fill='tozeroy', name='Not Placed', fillcolor='rgba(255, 99, 71, 0.5)')

    layout = go.Layout(title='Cumulative Placement Status by Branch',
                       xaxis=dict(title='Branch'),
                       yaxis=dict(title='Number of Students'))

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    graph_div = py.plot(fig, output_type='div', include_plotlyjs=False)
    return graph_div


def add_admin(request):
    form = AdminDetailForm()

    if request.method == 'POST':
        form = AdminDetailForm(request.POST, request.FILES)
        if form.is_valid():
            admin_email = form.cleaned_data['admin_email']
            admin_id = form.cleaned_data['admin_id']
            admin_password = form.cleaned_data['admin_password']

            # Check if email or admin_id already exists
            if User.objects.filter(email=admin_email).exists() or Admin.objects.filter(admin_id=admin_id).exists():
                messages.error(request, 'Email or Admin ID already exists.')
                return render(request, 'add_admin.html', {'form': form})
            
            # Create the User instance
            user = User.objects.create_user(
                username=admin_email,
                email=admin_email,
                password=admin_password,
                is_staff=True,  # Grant admin role
                is_superuser=False  # Not a superuser
            )
            
            # Create the Admin instance
            admin_instance = Admin(
                admin_id=admin_id,
                admin_name=form.cleaned_data['admin_name'],
                admin_email=admin_email,
                admin_password=admin_password,
                admin_branch=form.cleaned_data['admin_branch']
                # Add other fields as per your Admin model
            )
            admin_instance.save()
            
            # Send registration email to the admin
            subject = "Welcome to Our Admin Panel"
            message = f"Dear {admin_instance.admin_name},\n\nYou have been successfully added as an admin. Your admin ID is {admin_instance.admin_id}.\n\nThank you!"
            from_email = 'aniketsonkamble07@gmail.com'  
            recipient_list = [admin_email]
            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, 'Admin added successfully.')
            return redirect('admin_home')  
        
    return render(request, 'add_admin.html', {'form': form})

def admin_list(request):
    admins = Admin.objects.all()
    return render(request, 'admin_list.html', {'admins': admins})

def student_home(request):
    try:
        # Ensure the user has a student profile
        student = request.user.student
    except Student.DoesNotExist:
        # Handle the case where the user does not have a student profile
        messages.error(request, 'You need to complete your student profile to access job details.')
        return redirect('signup') 

    # Filter jobs based on the student's branch
    matching_jobs = JobDetail.objects.filter(required_branchs__icontains=student.branch)

    if matching_jobs.exists():
        return render(request, 'student_home.html', {'jobs': matching_jobs, 'student': student})
    else:
        messages.info(request, 'No job details available for your branch.')
        return render(request, 'student_home.html', {'student': student})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def studentlist(request,page=1):
    batch_year = request.GET.get('batch_year')
    students = Student.objects.all()

    if batch_year and batch_year.isdigit():
        students = students.filter(passing_year=batch_year)

    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    try:
        ServiceData = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ServiceData = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ServiceData = paginator.page(paginator.num_pages)

    batch_years = Student.objects.values_list('passing_year', flat=True).distinct()

    context = {
        'ServiceData': ServiceData,
        'batch_year': batch_year,
        'batch_years': batch_years,
    }
    return render(request, 'studentlist.html', context)


#  Excel sheet Download

def download_excel(request):
    batch_year = request.GET.get('batch_year')
    
    queryset = Student.objects.all()
    
    if batch_year:
        try:
            queryset = queryset.filter(passing_year=int(batch_year))
        except ValueError:
            # Handle invalid batch_year format gracefully, or log the error
            return HttpResponse('Invalid batch year format', status=400)
    
    xls_content = studentlist_xls(queryset)  # Pass queryset directly to studentlist_xls
    
    if xls_content:
        response = HttpResponse(xls_content, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=student_data.xls'
        return response
    else:
        return HttpResponse('Error generating Excel file', status=500)

# PDF Download
def download_pdf(request):
    batch_year = request.GET.get('batch_year')
    
    queryset = Student.objects.all()
    
    if batch_year:
        try:
            queryset = queryset.filter(passing_year=int(batch_year))
        except ValueError:
            # Handle invalid batch_year format gracefully, or log the error
            return HttpResponse('Invalid batch year format', status=400)
    
    context = {'ServiceData': queryset}
    
    # Generate PDF content
    pdf = render_to_pdf('studentlist_pdf.html', context)
    
    if pdf:
        # Serve PDF as response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=student_data.pdf'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Generate PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        pdf_file = result.getvalue()
        result.close()
        return pdf_file
    else:
        result.close()
        return None



def delete_std(request, crn_number, page=1):
    try:
        student = Student.objects.get(pk=crn_number)
    except Student.DoesNotExist:
        messages.error(request, "Student data not found")
        return HttpResponse("Student data not found", status=404)

    student_name = student.name

    # Check if the student has an associated user before trying to delete it
    if hasattr(student, 'user') and student.user is not None:
        student.user.delete()

    # Delete the Student object
    student.delete()
    messages.success(request, f"Student data for {student_name} deleted successfully.")

    return redirect("studentlist", page=page)
    

def update_std(request, crn_number):
    data = Student.objects.get(pk=crn_number)
    return render(request, "update_std.html", {'data': data})

def do_update_std(request, crn_number, page=1):
    # Get the student instance
    student_instance = get_object_or_404(Student, pk=crn_number)
    
    if request.method == 'POST':
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
        
        # Handle salary field
        salary = request.POST.get("salary", '00')  # Default value '00' if salary is not provided
        if not salary.strip():  # Check if salary is empty or contains only whitespace
            salary = '00'
        student_instance.salary = salary
        
        try:
            student_instance.save()
            messages.success(request, f'{student_instance.name} details updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating student details')
    
    return redirect("studentlist", page=page)

def add_job_details(request):
    if request.method == 'POST':
        form = JobDetailForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Process form data and save to the database
            job = form.save(commit=False)

            # Get the list of selected branches from the form
            selected_branches = request.POST.getlist('required_branchs')
            job.required_branchs = selected_branches
            
            # Get the passing year from the form
            passing_year = form.cleaned_data['required_passing_year']
            job.passing_year = passing_year
            job.save()

            # Filter students based on the selected branches and passing year
            students = Student.objects.filter(branch__in=selected_branches, passing_year=passing_year)
            subject = 'New Job Opening Alert'
            for student in students:
                message = f"""
                Dear {student.name},

                A new job opening has been posted: "{job.job_title}". Here are the job details:

                Job ID: {job.job_id}
                Title: {job.job_title}
                Company Name: {job.company_name}
                Salary: {job.salary}
                Location: {job.location}
                Date of Exam: {job.date_exam}
                Venue: {job.venue}

                Thank you for your interest.

                For more details, visit our website.

                Best regards,
                The PVG Placement Cell
                """
                from_email = "your-email@example.com"  # Update with your email
                to_email = student.email
                send_mail(subject, message, from_email, [to_email], fail_silently=False)

            messages.success(request, 'Job details added and emails sent successfully.')
            return redirect('job_list_admin', page=1)  # Redirect to admin job list view
        else:
            messages.error(request, 'Job details form is not valid. Please correct the errors and try again.')
    else:
        form = JobDetailForm()

    return render(request, 'add_job_details.html', {'form': form})

def job_list(request):
    try:
        # Ensure the user has a student profile
        student = request.user.student
    except Student.DoesNotExist:
        # Handle the case where the user does not have a student profile
        messages.error(request, 'You need to complete your student profile to access job details.')
        return redirect('profile_completion')  # Redirect to a profile completion page

    # Filter jobs based on the student's branch
    matching_jobs = JobDetail.objects.filter(required_branchs__icontains=student.branch)

    # Pagination setup
    paginator = Paginator(matching_jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')

    try:
        jobs = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)

    if matching_jobs.exists():
        return render(request, 'job_list.html', {'jobs': jobs, 'student': student})
    else:
        messages.info(request, 'No job details available for your branch.')
        return render(request, 'job_list.html', {'student': student})


def apply_for_job(request, job_id):
    job_detail = JobDetail.objects.get(pk=job_id)
    context = {'job_detail': job_detail, 'job_id': job_id}  
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
            if student.salary is not None and student.salary + 2.5 >= job.salary:
                messages.error(request, 'You  have already package in that range. You can not apply.')
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
        student_applications = JobApplication.objects.filter(student__crn_number=crn_number)
        
        if student_applications.exists():
            job_applications = JobDetail.objects.filter(
                jobapplication__student__crn_number=crn_number
            ).annotate(
                applied_time=F('jobapplication__applied_time'),
                is_present=F('jobapplication__is_present')
            )
            
            return render(request, 'applied_jobs.html', {'job_applications': job_applications})
        else:
            messages.error(request, "No applications found.")
            return redirect('student_home')
    else:
        messages.error(request, "CRN number not found in session.")
        return redirect('student_home')

def delete_job(request, job_id, page=1):
    job = get_object_or_404(JobDetail, pk=job_id)
    job_title = job.job_title  # Store the job title for the message
    job.delete()
    messages.success(request, f"Job '{job_title}' deleted successfully.")
    return redirect("job_list_admin", page=page)

def update_job(request, job_id):
    data = JobDetail.objects.get(pk=job_id)
    branches = ["IT", "ME", "CS", "EE", "ENTC", "Printing", "AIDS"]
    return render(request, "update_job.html", {'data': data, 'branches': branches})

def do_update_job(request, job_id, page=1):
    job_title = request.POST.get("job_title")
    company_name = request.POST.get("company_name")
    company_logo = request.FILES.get("company_logo")
    required_branchs = request.POST.getlist("required_branchs")
    salary = request.POST.get("salary")
    location = request.POST.get("location")
    required_CGPA = request.POST.get("required_CGPA")
    required_marks = request.POST.get("required_marks")
    date_exam = request.POST.get("date_exam")
    date_last = request.POST.get("date_last")
    venue = request.POST.get("venue")

    data = get_object_or_404(JobDetail, pk=job_id)

    try:

        
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

        messages.success(request, f"Job '{job_title}' updated successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while updating job '{job_title}': {str(e)}")

    return redirect("job_list_admin", page=page)


def job_list_admin(request, page=1):
    batch_year = request.GET.get('batch_year')
    jobs = JobDetail.objects.all().order_by('-system_time')

    if batch_year and batch_year.isdigit():
        jobs = jobs.filter(required_passing_year=batch_year)

    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')

    try:
        ServiceData = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ServiceData = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ServiceData = paginator.page(paginator.num_pages)

    batch_years = JobDetail.objects.values_list('required_passing_year', flat=True).distinct()

    context = {
        'ServiceData': ServiceData,
        'batch_year': batch_year,
        'batch_years': batch_years,
    }

    return render(request, 'job_list_admin.html', context)



def application_list_search(request):
    if request.method == 'GET':
        return render(request, 'application_list_search.html')

def application_list_search_result(request):
    search_applications = request.GET.get('search_applications')
    page_number = request.GET.get('page', 1)
    job_applications = []
    job_id = ''
    company_name = ''

    if search_applications:
        try:
            job_id = int(search_applications)
            job_applications = JobApplication.objects.filter(Q(job__job_id=job_id) | Q(job__job_title__icontains=search_applications))
        except ValueError:
            job_applications = JobApplication.objects.filter(job__job_title__icontains=search_applications)
            if job_applications.exists():
                job_id = job_applications.first().job.job_id

        if job_applications.exists():
            company_name = job_applications.first().job.company_name
        else:
            messages.error(request, 'No applications found for the given search term.')
            return redirect('application_list_search')

    if request.method == 'POST':
        application_ids = request.POST.getlist('application_ids')
        for app_id in application_ids:
            attendance_status = request.POST.get(f'attendance_status_{app_id}')
            salary = request.POST.get(f'salary_{app_id}')
            placement_status = 'On Campus'
            job_application = get_object_or_404(JobApplication, id=app_id)
            
            if attendance_status:
                job_application.is_present = attendance_status
                job_application.save()
            
            if salary is not None and salary != '':
                job_application.student.salary = salary
                job_application.student.placement_status = placement_status
                job_application.student.company_name = job_application.job.company_name
            else:
                job_application.student.salary = None
                job_application.student.placement_status = ''
                job_application.student.company_name = ''
                
            job_application.student.save()
                
        messages.success(request, 'Details updated successfully for all selected students.')

    paginator = Paginator(job_applications, 10)
    paginated_applications = paginator.get_page(page_number)

    context = {
        'students': paginated_applications,
        'job_id': job_id,
        'company_name': company_name,
        'search_applications': search_applications
    }
    return render(request, 'application_list_search_result.html', context)


def download_application_pdf(request, job_id):
    try:
        # Retrieve the job application based on the job_id or return a 404 error
        job_application = get_object_or_404(JobApplication, job__job_id=job_id)
    except JobApplication.DoesNotExist:
        # Handle case where no job application is found
        messages.error(request, 'No job application found with the given job ID.')
        return redirect('application_list_search')
    
    # Retrieve students who have applied for the specified job
    students = Student.objects.filter(jobapplication__job__job_id=job_id)
    
    if not students.exists():
        # Handle case where no students are found for the job application
        messages.error(request, 'No students found for the given job application.')
        return redirect('application_list_search')

    # Prepare context for rendering the PDF template
    context = {'students': students}
    
    # Generate PDF using render_to_pdf helper function
    pdf = render_to_pdf('application_list_pdf.html', context)
    
    if pdf:
        # If PDF generation is successful, create and return HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=student_data.pdf'
        return response
    else:
        # Handle case where PDF generation fails
        messages.error(request, 'Error generating PDF.')
        return redirect('application_list_search')



def download_application_excel(request, job_id):
    try:
        # Retrieve the job application based on the job_id
        job_application = get_object_or_404(JobApplication, job__job_id=job_id)
    except JobApplication.DoesNotExist:
        # Handle case where no job application is found
        messages.error(request, 'No job application found with the given job ID.')
        return redirect('application_list_search')
    
    # Retrieve students who have applied for the specified job
    students = Student.objects.filter(jobapplication__job__job_id=job_id)
    
    if not students.exists():
        # Handle case where no students are found for the job application
        messages.error(request, 'No students found for the given job application.')
        return redirect('application_list_search')

    # Generate Excel content using the custom function
    xls_content = studentlist_xls(students)

    # Create HTTP response for Excel download
    response = HttpResponse(xls_content, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=student_data.xls'
    return response


def placement_list(request):
    placements = Placement.objects.all()
    return render(request, 'placement_list.html', {'placements': placements})



def add_placement(request):
    crn_number = request.session.get('crn_number')
    try:
        student = Student.objects.get(pk=crn_number)
    except Student.DoesNotExist:
        messages.error(request, "Session expired, please log in again!")
        return redirect('student_home')
    
    if request.method == 'POST':
        form = PlacementForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Placement information updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "There was an error updating the placement information. Please check the form and try again.")
    else:
        form = PlacementForm(instance=student)
    
    return render(request, 'add_placement.html', {'form': form})

