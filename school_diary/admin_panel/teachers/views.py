from django.shortcuts import render, redirect
from diary.decorators import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from diary import models
from admin_panel.teachers import forms


@login_required(login_url="/login/")
@admin_only
def teachers_dashboard_first_page(request):
    return redirect('teachers_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def teachers_dashboard(request, page):
    u = models.Teachers.objects.all()
    if request.method == "POST":
        fn = request.POST.get('first_name')
        s = request.POST.get('surname')
        email = request.POST.get('email')
        u = u.filter(
            first_name__icontains=fn, surname__icontains=s,
            account__email__icontains=email)
    u = Paginator(u, 50)
    u = u.get_page(page)
    return render(request, 'teachers/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def teachers_delete(request, id):
    """
    Delete a teacher.
    """
    u = models.Users.objects.get(email=id)
    s = models.Teachers.objects.get(account=u)
    if request.method == "POST":
        u.delete()
        s.delete()
        return redirect('teachers_dashboard')
    return render(request, 'teachers/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def teachers_update(request, id):
    """
    Edit teachers's account info.
    """
    u = models.Users.objects.get(email=id)
    s = models.Teachers.objects.get(account=u)
    if request.method == "POST":
        form = forms.TeacherEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('teachers_dashboard')
    form = forms.TeacherEditForm(instance=s)
    return render(request, 'teachers/update.html', {'form': form})
