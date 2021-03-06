from django.shortcuts import render, redirect
from diary.decorators import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from diary import models
from admin_panel.students import forms


@login_required(login_url="/login/")
@admin_only
def students_dashboard_first_page(request):
    return redirect('students_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def students_dashboard(request, page):
    """
    Send a dashboard with up to 100 students.
    """
    students = models.Students.objects.all()
    grades = models.Grades.objects.all()
    if request.method == "POST":
        fn = request.POST.get('first_name')
        s = request.POST.get('surname')
        email = request.POST.get('email')
        grade = int(request.POST.get('class'))
        if grade == -1:
            grade = None
        if grade == -2:  # Grade isn't chosen
            kwargs = {}
        else:
            kwargs = {"grade": grade}
        students = students.filter(
            first_name__icontains=fn, surname__icontains=s,
            account__email__icontains=email, **kwargs)
    students = Paginator(students, 100)
    students = students.get_page(page)
    context = {'students': students, 'classes': grades}
    return render(request, 'students/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def students_delete(request, id):
    """
    Delete a student.
    """
    u = models.Users.objects.get(email=id)
    s = models.Students.objects.get(account=u)
    if request.method == "POST":
        u.delete()
        s.delete()
        return redirect('students_dashboard')
    return render(request, 'students/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def students_update(request, id):
    """
    Edit student's account info.
    """
    u = models.Users.objects.get(email=id)
    s = models.Students.objects.get(account=u)
    if request.method == "POST":
        form = forms.StudentEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('students_dashboard')
    form = forms.StudentEditForm(instance=s)
    return render(request, 'students/update.html', {'form': form})
