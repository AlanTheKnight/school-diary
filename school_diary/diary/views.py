from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import StudentSignUpForm, UserLogin, AdminSignUpForm, TeacherSignUpForm
from .decorators import unauthenticated_user, admin_only
from django.contrib.auth.decorators import login_required


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
    form = UserLogin()
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('/diary/login/')


def user_profile(request):
    context = {}
    return render(request, 'profile.html', {})


@login_required(login_url="/diary/login/")
def diary(request):
    if request.user.account_type == 0:
        return render(request, 'diary_admin_main.html')
    else:
        context = {}
        return render(request, 'diary.html', context)


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
            messages.success(request, "Новый администратор был создан успешно.")
            return redirect('/diary/login/')
    if request.POST:
        form = TeacherSignUpForm(request.POST)
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration_teacher.html', {'form': form, 'error': 0})