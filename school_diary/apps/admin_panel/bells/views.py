import datetime
import json
from django.shortcuts import render, redirect, HttpResponse
from apps.core.access import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.admin_panel.bells import forms
from apps.timetable import models


SCHOOLS = dict([
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
])


@login_required(login_url="/login/")
@admin_only
def bells_dashboard_first_page(request):
    return redirect('bells_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def bells_dashboard(request, page):
    objects = models.BellsTimeTable.objects.all()
    amount = len(objects)
    objects = Paginator(objects, 100)
    objects = objects.get_page(page)
    context = {
        "objects": objects,
        "amount": amount,
        "wiki": "help/",
        "title": " Расписание звонков",
        "schools": SCHOOLS
    }
    return render(request, 'bells/../bells/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def bells_delete(request, pk):
    obj = models.BellsTimeTable.objects.get(pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect('bells_dashboard')
    context = {
        "object": obj,
        "help_text": "Вы уверены, что хотите удалить эту запись?"
    }
    return render(request, 'bells/../bells/delete.html', context)


@login_required(login_url="/login/")
@admin_only
def bells_update(request, pk):
    obj = models.BellsTimeTable.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.BellCreateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('bells_dashboard')
    form = forms.BellCreateForm(instance=obj)
    return render(request, 'bells/../bells/create.html', {'form': form, 'title': "Добавить звонок"})


@login_required(login_url="/login/")
@admin_only
def bells_create(request):
    if request.method == "POST":
        form = forms.BellCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bells_dashboard')
    form = forms.BellCreateForm()
    return render(request, 'bells/../bells/create.html', {'form': form, 'title': "Добавить звонок"})


@login_required(login_url="/login/")
@admin_only
def bells_table(request):
    return render(request, 'bells/../bells/table.html')


@login_required(login_url="/login/")
@admin_only
def bells_table_save(request):
    if request.is_ajax and request.method == "POST":
        sch = request.POST.get('school')
        s = 1 if sch == "Младшая школа" else 2
        lsnlist = request.POST.get("lsnlist")[9:].split("&")[:-1]
        time_format = "%H:%M"
        for lsn in lsnlist:
            lsninfo = request.POST.get(lsn).split("&")
            begin = lsninfo[0]
            end = lsninfo[1]
            if begin == '':
                begin = datetime.strptime('00:00', time_format)
            if end == '':
                end = datetime.strptime('00:00', time_format)
            if models.BellsTimeTable.objects.filter(school=s, n=lsn).exists():
                bell = models.BellsTimeTable.objects.get(school=s, n=lsn)
                if bell.start != begin or bell.end != end:
                    bell.start = begin
                    bell.end = end
                    bell.save()
            else:
                bell = models.BellsTimeTable.objects.create(
                    school=s, n=lsn, start=begin, end=end)
        return HttpResponse('ok')
    elif request.is_ajax and request.method == "GET":
        s = request.GET.get("school")
        sch = 1 if s == "Младшая школа" else 2
        b = models.BellsTimeTable.objects.filter(school=sch)
        data = {}
        for Bell in b:
            data[Bell.n] = [str(Bell.start)[:-3], str(Bell.end)[:-3]]
        jsondata = json.dumps(data)
        return HttpResponse(jsondata)
