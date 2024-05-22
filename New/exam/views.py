from django.shortcuts import render,redirect,reverse

# from exam.models import SignUp
from .models import *

from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
# from django.contrib.auth.models import SignUp








# done by me

# from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
# from datetime import date











# Done by ujjwal
def notes_sharing(request):
    # return render(request,'notes_sharing/notes_home.html')
    return render(request,'notes_sharing/index.html')
    # return render(request,'notes_sharing/navigation.html')



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    # 'total_course':models.Course.objects.all().count(),
    # 'total_question':models.Question.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'exam/salary_form.html',{'teacherSalary':teacherSalary})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher_salary.html',{'teachers':teachers})




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'exam/admin_course.html')


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})






















# Create your views here.

def about(request):
    return render(request, 'notes_sharing/about.html')

def home(request):
    return render(request, 'notes_sharing/index.html')

def userlogin(request):
    # print("userlogin reached")
    # return
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        # print("userlogin auth reached")
        # return render(request, 'notes_sharing/login.html', {'error':"no"})
        try:
            if user:
                login(request, user)
                # print("login caller")
                # return
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'notes_sharing/login.html', d)

def login_admin(request):
    return render(request, 'notes_sharing/login_admin.html')

# def signup1(request):
#     error = ""
#     if request.method == "POST":
#         f = request.POST['fname']
#         l = request.POST['lname']
#         n = request.POST['con']
#         e = request.POST['emailid']
#         p = request.POST['pwd']
#         c = request.POST['cls']
#         r = request.POST['role']
#         try:
#             user = User.objects.create_user(username = e, password = p, first_name = f, last_name =l)
#             s.objects.create(user = user, contact = n, branch = c, role = r)
#             error = "no"
#         except:
#             error = "yes"
#     d = {'error' : error}
#     return render(request, 'notes_sharing/signup.html', d)

def admin_home(request):
    # if not request.user.is_staff:
    #     return redirect('login_admin')
    pn = Notes.objects.filter(status = "Pending").count()
    an = Notes.objects.filter(status = "Accept").count()
    rn = Notes.objects.filter(status = "Reject").count()
    alln = Notes.objects.all().count()
    d = {'pn' : pn, 'an' : an, 'rn' : rn, 'alln' : alln}
    return render(request, 'notes_sharing/admin_home.html', d)


def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        # user = authenticate(username = u, password = p)
        try:
            error="no"
            # if user.is_staff:
            #     login(request, user)
            #     error = "no"
            # else:
            #     error = "yes"
        except:
            error = "yes"
    d = {'error' : error}
    return render(request, 'notes_sharing/login_admin.html', d)

def Logout(request):
    logout(request)
    return redirect('index')


from exam.models import SignUp as s

def profile(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    user = User.objects.get(id = request.user.id)
    print("checkState usernam:")
    print(user)
    # print(user['contact'])
    # data = SignUp.objects.filter(user=request.user.id)
    # data = SignUp.objects.get(user = user.id)
    # data = SignUp.objects.all()
    # data = s.objects.get()
    # print(data.first)
    # d = {'data' : data,'user' : user}
    # data = forms.models.SignUp.objects.all()
    d = {'data':{},'user':user}
    # print(data.model.branch)
    # print(user.username)
    # print(user.email)
    # print(user.contact)
    # return render(request, 'notes_sharing/about.html', d)
    return render(request, 'notes_sharing/profile.html', d)

def edit_profile(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
    user = User.objects.get(id = request.user.id)
    # data = SignUp.objects.get(user = user)
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        n = request.POST['contact']
        c = request.POST['branch']
        user.first_name = f
        user.last_name = l
        # data.contact = n
        # data.branch = c
        user.save()
        # data.save()
    #     error = True
    # d = {'data' : data, 'user' : user, 'error' : error}
    return render(request, 'notes_sharing/edit_profile.html', {})

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method == "POST":
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c == n:
            u = User.objects.get(username__exact = request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d = {'error' : error}
    return render(request, 'notes_sharing/change_password.html', d)

def upload_notes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    error = ""
    if request.method == "POST":
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        des = request.POST['description']
        u = User.objects.filter(username = request.user.username).first()
        # u = User.objects.filter(username = {"ishu"}).first()
        try:
            Notes.objects.create(user = u, uploadingdate = date.today(), branch = b, subject = s, notesfile = n, filetype = f, description = des, status = 'Pending')
            error = "no"
        except:
            error = "yes"
    courseNames = Course.objects.all()
    print("Course upload")
    print(courseNames)
    # return
    d = {'error' : error,'subjects':courseNames}
    return render(request, 'notes_sharing/upload_notes.html', d)

def view_mynotes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    userType=""
    if is_student(request.user): 
        userType = "student"     
    if is_teacher(request.user): 
        userType = "teacher"     
    user = User.objects.get(id = request.user.id)
    notes = Notes.objects.filter(user = user)
    

    d = {'notes' : notes,"userType":userType}
    return render(request, 'notes_sharing/view_mynotes.html', d)

def delete_mynotes(request, pid):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    notes = Notes.objects.get(id = pid)
    notes.delete()
    return redirect('view_mynotes')

def view_users(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_admin')
    users = SignUp.objects.all()
    d = {'users' : users}
    return render(request, 'notes_sharing/view_users.html', d)

def delete_users(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id = pid)
    user.delete()
    return redirect('view_users')

def pending_notes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_admin')
    notes = Notes.objects.filter(status = "Pending")
    d = {'notes' : notes}
    return render(request, 'notes_sharing/pending_notes.html', d)

def accepted_notes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_admin')
    notes = Notes.objects.filter(status = "Accept")
    d = {'notes' : notes}
    return render(request, 'notes_sharing/accepted_notes.html', d)

def rejected_notes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_admin')
    notes = Notes.objects.filter(status = "Reject")
    d = {'notes' : notes}
    return render(request, 'notes_sharing/rejected_notes.html', d)

def all_notes(request):
    # return viewallnotes
    # if not request.user.is_authenticated:
    #     return redirect('login_admin')
    notes = Notes.objects.all()
    d = {'notes' : notes}
    return render(request, 'notes_sharing/all_notes.html', d)

def assign_status(request, pid):
    # if not request.user.is_authenticated:
    #     return redirect('login_admin')
    notes = Notes.objects.get(id = pid)
    error = ""
    if request.method == "POST":
        s = request.POST['status']
        try:
           notes.status = s
           notes.save()
           error = "no"
        except:
            error = "yes"
    d = {'notes': notes, 'error' : error}
    return render(request, 'notes_sharing/assign_status.html', d)

def delete_notes(request, pid):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    notes = Notes.objects.get(id = pid)
    notes.delete()
    return redirect('all_notes')

def viewallnotes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    userType = ""
    if is_teacher(request.user): 
        userType = "TEACHER"
    if is_student(request.user): 
        userType = "student"     
    notes = Notes.objects.filter(status = "Accept")
    d = {'notes' : notes,"userType":userType}
    return render(request, 'notes_sharing/viewallnotes.html', d)



def viewStudentnotes(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    # courseNames = ['b.tech','bca','mca','B.Sc','B.A','B.A.F','B.Com','B.M.S','B.B.I']
    notes = Notes.objects.filter(status = "Accept")
    courses = Course.objects.all()
    # length = len(courses)
    # await fetchCourseNotes()
    # courseWiseNotes = {}
    print("fetching notes data")
    # print(courses[0].course_name)
    # for i in range(0,len(notes)):
    #     courseWiseNotes[notes[i].branch] = notes[i]
    #     print(notes[i].branch)

        # if i.branch==courseName:
        #     courseNotes.append(i)
    d = {'notes' : notes,'courseNames':courses}
    return render(request, 'notes_sharing/student_course.html', d)





def fetchCourseNotes(request,courseName):
    print("Coursename:")
    print(courseName)
    notes = Notes.objects.filter(status = "Accept")
    # courses = Course.objects.all()
    courseNotes = []
    for i in notes:
        if i.subject==courseName:
            courseNotes.append(i)
    d = {'notes' : courseNotes}
    return render(request, 'notes_sharing/course_notes.html', d)
