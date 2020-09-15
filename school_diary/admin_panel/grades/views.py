from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.db.models import ProtectedError

from diary.decorators import admin_only
from diary import models

from . import forms


MODEL = models.Grades
FORM = forms.GradeCreationForm
FILTER = None
PER_PAGE = 100
DATA = {
    'dashboard': {
        'title': 'Классы',
        'template': 'grades/dashboard.html',
        'url': 'grades:dashboard',
        'fields': [
            'Класс',
            'Классный руководитель',
            'Предметы',
            'Учителя',
        ],
        'create_text': "Создать новый класс",
    },
    'delete': {
        'title': 'Удалить класс',
        'template': 'grades/delete.html',
        'url': 'grades:delete',
    },
    'update': {
        'title': '',
        'template': 'grades/update.html',
        'url': 'grades:update',
    }
}


@login_required(login_url="/login/")
@admin_only
def dashboard_first_page(request):
    return redirect(DATA['dashboard']['url'], page=1)


@login_required(login_url="/login/")
@admin_only
def dashboard(request, page):
    if request.method == "POST":
        form = FORM(request.POST)
        if form.is_valid():
            form.save()
            return redirect(DATA['dashboard']['url'])
    form = FORM()
    objects = MODEL.objects.all()
    amount = MODEL.objects.count()
    objects = Paginator(objects, PER_PAGE)
    objects = objects.get_page(page)
    context = {
        "objects": objects,
        "amount": amount,
        "form": form,
        "title": DATA['dashboard']['title'],
        "fields": DATA['dashboard']['fields'],
        "create_text": DATA['dashboard']['create_text']
    }
    return render(request, DATA['dashboard']['template'], context)


@login_required(login_url="/login/")
@admin_only
def delete(request, pk):
    obj = MODEL.objects.get(pk=pk)
    context = {"object": obj}
    if request.method == "POST":
        try:
            obj.delete()
        except ProtectedError:
            context["protected"] = True
            return render(request, DATA['delete']['template'], context)
        return redirect(DATA['dashboard']['url'])
    return render(request, DATA['delete']['template'], context)


@login_required(login_url="/login/")
@admin_only
def update(request, pk):
    obj = MODEL.objects.get(pk=pk)
    if request.method == "POST":
        form = FORM(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(DATA['dashboard']['url'])
    form = forms.GradeCreationForm(instance=obj)
    context = {
        'form': form,
        'title': DATA['update']['title']
    }
    return render(request, DATA['update']['template'], context)
