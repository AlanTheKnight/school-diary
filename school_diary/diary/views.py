from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .models import Students
from .forms import StudentCreationForm, StudentsLogin
from django.http import HttpResponseRedirect, HttpResponse


def students_registration(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            form = StudentCreationForm()
            return render(request, 'registration.html', {'form': form, 'display': 'block'})
    else:
        form = StudentCreationForm()
        return render(request, 'registration.html', {'form': form, 'display': 'none'})


def students_login(request):
    if request.method == 'POST':
        form = StudentsLogin(request.POST)
        if form.is_valid():
            user = Students.objects.get(email=form.cleaned_data['email'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('not login')
        else:
            form = StudentsLogin()
            # return render(request, 'login.html', {'form': form, 'display': 'block'})

    else:
        form = StudentsLogin()
        return render(request, 'login.html', {'form': form})