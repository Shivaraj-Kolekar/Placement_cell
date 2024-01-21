
from django.urls import path
from .import views
from .views import  update_job_details, actual_update_job_details, add_job_details

urlpatterns = [
     path("",views.index,name="PVG HOME"),
     path('signup/', views.signup, name='signup'),
     path('job_list/',views.job_list, name='job_list'),
     path('add_job_details/', views.add_job_details, name='add_job_details'),
     path('list/',views.list,name='list'),
     path('admin_home/',views.admin_home,name='admin_home'),
     path('update_job_details/', update_job_details, name='update_job_details'),
     path("actual_update_job_details/",views.actual_update_job_details, name="actual_update_job_details")
]
