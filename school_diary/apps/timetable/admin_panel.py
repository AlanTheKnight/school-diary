from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.access import admin_only
from apps.timetable import forms
from apps.timetable import models
from apps.timetable import utils


SCHOOLS = dict([
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
])


@login_required(login_url='/login/')
@admin_only
def dashboard(request):
    form = forms.GetTimeTableForm()
    my_klass = models.Klasses.objects.get_or_create(number=1, letter="А")[0]
    lessons = models.Lessons.objects.filter(klass=my_klass).order_by('day', 'number')
    context = {
        'form': form,
        'lessons': lessons,
        'klass': my_klass,
    }
    return render(request, 'timetable/dashboard.html', context)
