
from django.urls import path
from .import views


#from .views import  update_job_details, actual_update_job_details, add_job_details

urlpatterns = [
     path("",views.index,name="PVG HOME"),
     path('signup/', views.signup, name='signup'),
     path('student_login/',views.student_login,name='student_login'),
     path("student_home/",views.student_home,name="student_home"),
     path("my_logout/",views.my_logout,name="my_logout"),

     path('job_list/',views.job_list, name='job_list'),
     path('add_job_details/', views.add_job_details, name='add_job_details'),
     path('list/',views.list,name='list'),
     path('admin_home/',views.admin_home,name='admin_home'),
     path('update_job_details/', views.update_job_details, name='update_job_details'),
     path("actual_update_job_details/<int:job_id>",views.actual_update_job_details, name="actual_update_job_details"),
     
     path("my_view/<int:page>", views.my_view, name="my_view"),
     path("my_view/", views.my_view, name="my_view_default"),
     
     path("studentlist/<int:page>", views.studentlist, name="studentlist"),
     path("studentlist/", views.studentlist, name="studentlist_default"),

      path('apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
     path('download_excel/', views.download_excel, name='download_excel'),
     path('download_pdf/', views.download_pdf, name='download_pdf'),

]
