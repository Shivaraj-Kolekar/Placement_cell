
from django.urls import path
from .import views

urlpatterns = [
     path("",views.index,name="PVG HOME"),
     path('signup/', views.signup, name='signup'),
     path('job_list/',views.job_list, name='job_list'),
     path('add_job_details/', views.add_job_details, name='add_job_details'),
    
]
