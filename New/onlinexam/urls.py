# from django.conf import settings
from django.urls import path,include
from django.contrib import admin
from onlinexam import settings
from exam import views
from django.contrib.auth.views import LogoutView,LoginView
from django.conf.urls.static import static

urlpatterns = [
    # done by ujjwal
    # path('ujjwal_notes_share',views.notes_homePage,name='notes_share_any_name'),

    
    path('admin_dashboard',views.admin_dashboard_view,name='admin_dashboard'),


    # path('home', views.notes_homePage,name='home'),
    path('about', views.about, name='about'),
    path('login', views.userlogin, name='login'),
    # path('signup', views.signup1, name='signup'),
    path('login_admin', views.login_admin, name='login_admin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('logout', views.Logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('upload_notes', views.upload_notes, name='upload_notes'),
    path('pending_notes', views.pending_notes, name='pending_notes'),
    path('accepted_notes', views.accepted_notes, name='accepted_notes'),
    path('rejected_notes', views.rejected_notes, name='rejected_notes'),
    path('all_notes', views.all_notes, name='all_notes'),
    path('delete_mynotes/<int:pid>', views.delete_mynotes, name='delete_mynotes'),
    path('delete_notes/<int:pid>', views.delete_notes, name='delete_notes'),
    path('delete_users/<int:pid>', views.delete_users, name='delete_users'),
    path('assign_status/<int:pid>', views.assign_status, name='assign_status'),
    path('view_users', views.view_users, name='view_users'),
    path('view_mynotes', views.view_mynotes, name='view_mynotes'),
    path('viewallnotes', views.viewallnotes, name='viewallnotes'),
    path('', views.home_view, name='index'),
    # path('courseNotes/<Course:courseName>', views.fetchCourseNotes,name='courseNotes'),
   

























    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),



    


    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='exam/logout.html'),name='logout'),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),

    path('admin-course', views.admin_course_view,name='admin-course'),
    path('admin-add-course', views.admin_add_course_view,name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view,name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view,name='delete-course'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)