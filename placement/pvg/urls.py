
from django.urls import path
from .import views


#from .views import  update_job_details, actual_update_job_details, add_job_details

urlpatterns = [
     path("",views.index,name="PVG HOME"),
     
     path('signup/', views.signup, name='signup'),
     path('login/',views.student_login,name='student_login'),
     path("student_home/",views.student_home,name="student_home"),
     path("my_logout/",views.my_logout,name="my_logout"),

     path('job_list/',views.job_list, name='job_list'),
     path('add_job_details/', views.add_job_details, name='add_job_details'),
     path('list/',views.list,name='list'),
     path('admin_home/',views.admin_home,name='admin_home'),
     path('add_admin/',views.add_admin,name='add_admin'),
     
     path('job_list_admin/<int:page>/', views.job_list_admin, name='job_list_admin'),

     path("job_list_admin/", views.job_list_admin, name="job_list_admin_default"),
     
     path("delete_job/<int:job_id>",views.delete_job,name="delete_job"),
     path("update_job/<int:job_id>",views.update_job,name="update_job"),
     path("do_update_job/<int:job_id>",views.do_update_job,name="do_update_job"),


     path("studentlist/<int:page>", views.studentlist, name="studentlist"),
     path("studentlist/", views.studentlist, name="studentlist_default"),
     path('applied_jobs/', views.applied_jobs, name='applied_jobs'),

     path("delete_std/<int:crn_number>",views.delete_std,name="delete_std"),
     path("update_std/<int:crn_number>",views.update_std,name="update_std"),
     path("do_update_std/<int:crn_number>",views.do_update_std,name="do_update_std"),

     path('apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
     path('download_excel/', views.download_excel, name='download_excel'),
     path('download_pdf/', views.download_pdf, name='download_pdf'),

     path('apply_for_job2/<int:job_id>/', views.apply_for_job2, name='apply_for_job2'),

     path('application_list_search/',views.application_list_search,name="application_list_search"),
     path('application_list_search_result/', views.application_list_search_result ,name="application_list_search_result"),
     path('download_application_pdf/<int:job_id>/',views.download_application_pdf, name='download_application_pdf'),
    path('download_application_excel/<int:job_id>/',views.download_application_excel, name='download_application_excel') ,


     path('placements/', views.placement_list, name='placement_list'),
    path('add_placement/', views.add_placement, name='add_placement'),
]
