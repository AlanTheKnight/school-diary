from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# from .models import Students
# from .forms import StudentCreationForm, StudentsLogin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .forms import StudentSignUpForm, StudentsLogin


def students_registration(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/diary/login')
    if request.POST:
        form = StudentSignUpForm(request.POST)
    else:
        form = StudentSignUpForm()
    return render(request, 'registration.html', {'form': form, 'error': 0})


def students_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            print("Registration was successful")
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Username OR password is incorrect')
    form = StudentsLogin()
    return render(request, 'login.html', {'form': form})
