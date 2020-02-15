from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
# from .forms import StudentSignUpForm, StudentsLogin
from .models import Students, Teachers, Subjects
from .forms import StudentSignUpForm, UsersLogin, AdminSignUpForm, TeacherSignUpForm
from .decorators import unauthenticated_user, admin_only
from django.contrib.auth.decorators import login_required
from .models import *


@unauthenticated_user
def user_register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Учётная запись была создана успешно.")
            return redirect('/diary/login')
    if request.POST:
        form = StudentSignUpForm(request.POST)
    else:
        form = StudentSignUpForm()
    return render(request, 'registration.html', {'form': form, 'error': 0})


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Неправильный адрес электронной почты или пароль.')
    form = UsersLogin()
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('/diary/login/')


@login_required(login_url="/diary/login/")
def user_profile(request):
    if request.user.account_type == 0:
        data = Users.objects.get(email=request.user)
    if request.user.account_type == 1:
        data = Administrators.objects.get(account=request.user)
    if request.user.account_type == 2:
        data = Teachers.objects.get(account=request.user)
    if request.user.account_type == 3:
        data = Students.objects.get(account=request.user)
    context = {'data':data}
    return render(request, 'profile.html', context)


@login_required(login_url="/diary/login/")
@admin_only
def admin_register(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый администратор был создан успешно.")
            return redirect('/diary/login/')
    if request.POST:
        form = AdminSignUpForm(request.POST)
    else:
        form = AdminSignUpForm()
    return render(request, 'registration_admin.html', {'form': form, 'error': 0})


@login_required(login_url="/diary/login/")
@admin_only
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый учитель был создан успешно.")
            return redirect('/diary/login/')
    if request.POST:
        form = TeacherSignUpForm(request.POST)
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration_teacher.html', {'form': form, 'error': 0})


@login_required(login_url="/diary/login/")
def diary(request):
    if request.user.account_type == 0 or request.user.account_type == 1:
        return render(request, 'diary_admin_main.html')

    elif request.user.account_type == 3:
        student = Students.objects.get(account=request.user)
        context = {'Student': student,
                   'subjects': Subjects.objects.all(),
                   'daylist': ['09.02', '10.02', '11.02'],
                   'marks': student.mark_set.order_by('date')}
        return render(request, 'student.html', context)

    elif request.user.account_type == 2:
        teacher = Teachers.objects.get(account=request.user)
        context = {'Teacher': teacher,
                   'subjects': teacher.subjects.all(),
                   'grades': Grades.objects.filter(teachers=teacher),
                   'is_post': False
                   }

        if request.method == 'POST':
            subject = Subjects.objects.get(name=request.POST.get('subject'))
            number = int(request.POST.get('grade')[0])
            letter = request.POST.get('grade')[1]
            try:
                grade = Grades.objects.get(number=number, subjects=subject, letter=letter, teachers=teacher)
            except:
                messages.error(request, 'Ошибка')
                return render(request, 'teacher.html', context)

            lessons = Lessons.objects.filter(grade=grade, subject=subject)
            students = Students.objects.filter(grade=grade)
            scope = {}
            for student in students:
                for_lesson = []
                for lesson in lessons:
                    try:
                        for_lesson.append(student.marks_set.get(lesson=lesson))
                    except:
                        for_lesson.append(None)
                scope.update({student: for_lesson})
            context.update({
                'is_post': True,
                'lessons': lessons,
                'scope': scope
            })
            return render(request, 'teacher.html', context)
        else:
            return render(request, 'teacher.html', context)
    else:
        redirect('/')

