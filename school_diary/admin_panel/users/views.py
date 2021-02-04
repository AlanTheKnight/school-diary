from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from core.access import admin_only
from core import models
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
def messages(request, page=1):
    m = Paginator(models.AdminMessages.objects.all(), 50).get_page(page)
    context = {"messages": m}
    return render(request, "admin_panel/users/messages.html", context)


@login_required(login_url="/login/")
@admin_only
def message(request, pk: int):
    m = models.AdminMessages.objects.get(pk=pk)
    context = {"m": m}
    return render(request, "admin_panel/users/message.html", context)
