from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from apps.core import models
from apps.core.access import admin_only
from apps.core.users import forms
from .forms import FilterForm


@login_required(login_url="/login/")
@admin_only
def main(request, page=1):
    messages_qs = models.AdminMessages.objects.filter(is_read=False).count()
    users = models.Users.objects.all()
    filter_form = FilterForm()
    t = -1
    if request.method == "POST":
        filter_form = FilterForm(request.POST)
        t = int(filter_form.data['usertype'])
    if t != -1:
        users = users.filter(account_type=t)
    users = Paginator(users, 50).get_page(page)
    context = {
        "form": filter_form,
        "users": users,
        "t": t,
        "messages": messages_qs,
    }
    return render(request, 'admin_panel/users/users.html', context)


@login_required(login_url="/login/")
@admin_only
def edit(request, pk: int):
    u = models.Users.objects.get(pk=pk)
    form = u.get_edit_form(instance=u)
    if request.method == "POST":
        form = u.get_edit_form(instance=u, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:users")
    context = {"form": form}
    return render(request, 'admin_panel/users/edit.html', context)


@login_required(login_url="/login/")
@admin_only
def admin_messages(request, page=1):
    m = Paginator(models.AdminMessages.objects.all(), 50).get_page(page)
    context = {"messages": m}
    return render(request, "admin_panel/users/messages.html", context)


@login_required(login_url="/login/")
@admin_only
def message_details(request, pk: int):
    message = get_object_or_404(models.AdminMessages, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {"m": message}
    return render(request, "admin_panel/users/message.html", context)


@login_required(login_url="/login/")
@admin_only
def message_delete(request, pk: int):
    message = get_object_or_404(models.AdminMessages, pk=pk)
    if request.method == "POST":
        message.delete()
        return redirect('users:messages')
    return render(request, 'admin_panel/users/delete.html', {'obj': message})


@login_required(login_url="/login/")
@admin_only
def register_admin(request):
    form = forms.AdminSignUpForm()
    if request.method == 'POST':
        form = forms.AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Новый аккаунт администратора был создан успешно.")
            return redirect('login')
    return render(request, 'admin_panel/users/register_admin.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def register_teacher(request):
    form = forms.TeacherSignUpForm()
    if request.method == 'POST':
        form = forms.TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Новый аккаунт учителя был создан успешно.")
            return redirect('login')
    return render(request, 'admin_panel/users/register_teacher.html', {'form': form})
