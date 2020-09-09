from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from diary.decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib import messages
from . import forms
from diary import models
from diary.decorators import student_only


@unauthenticated_user
def user_register(request):
    """
    New student registration.
    """
    if request.method == 'POST':
        form = forms.StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Учётная запись была создана успешно.")
            return redirect('login')
    if request.method != 'POST':
        form = forms.StudentSignUpForm()
    return render(request, 'registration.html', {'form': form})


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(
                request, 'Неправильный адрес электронной почты или пароль.')
    form = forms.UsersLogin()
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url="/login/")
def user_profile(request):
    """
    User profile page (diary56.ru/profile/)
    """
    if request.user.account_type == 2:
        if request.method == "POST":
            if 'image-upload' in request.POST:
                request.user.teacher.avatar = request.FILES.get('avatar')
                request.user.teacher.save()
            elif 'image-delete' in request.POST:
                request.user.teacher.avatar.delete()
    return render(request, 'profile.html')


@login_required(login_url="/login/")
@admin_only
def admin_register(request):
    if request.method == 'POST':
        form = forms.AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Новый аккаунт администратора был создан успешно.")
            return redirect('login')
    if request.POST:
        form = forms.AdminSignUpForm(request.POST)
    else:
        form = forms.AdminSignUpForm()
    context = {'form': form, 'error': 0}
    return render(request, 'registration_admin.html', context)


@login_required(login_url="/login/")
@admin_only
def teacher_register(request):
    if request.method == 'POST':
        form = forms.TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Новый аккаунт учителя был создан успешно.")
            return redirect('login')
    if request.POST:
        form = forms.TeacherSignUpForm(request.POST)
    else:
        form = forms.TeacherSignUpForm()
    context = {'form': form, 'error': 0}
    return render(request, 'registration_teacher.html', context)


@allowed_users(
    allowed_roles=['teachers', 'students'],
    message="Администраторы не имеют доступ к этой странице.")
@login_required(login_url="login")
def admin_message(request):
    """
    Send a message to an admin.
    """
    if request.method == "POST":
        form = forms.AdminMessageCreationForm(request.POST)
        if form.is_valid():
            m = form.save()
            m.sender = request.user
            m.save()
            return redirect('profile')
    form = forms.AdminMessageCreationForm()
    return render(request, 'admin_messages.html', {'form': form})


@student_only
def teacher_page(request, pk: int):
    t = get_object_or_404(models.Teachers, account_id=pk)
    context = {'teacher': t}
    return render(request, "teacher_page.html", context)
