from django.shortcuts import render, get_object_or_404
from urllib.parse import unquote
from .forms import GetTimeTableForm, LessonCreateForm, BellCreateForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Grades, Lessons, BellsTimeTable
import time
import json
from .decorators import admin_only
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .forms import GetTimeTableForm
from django.http import HttpResponseRedirect
from .models import Grades, Lessons
import time
from collections import OrderedDict


DAYWEEK_NAMES = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}


def timetable(request):
    """Gets grade from form and redirects to the page showing its timetable."""
    if request.method == 'POST':
        form = GetTimeTableForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_litera = form.cleaned_data['litera']
            url = str(chosen_grade) + '/' + chosen_litera
            url = unquote(url)
            return HttpResponseRedirect(url)
    else:
        form = GetTimeTableForm()
        return render(request, 'timetable/timetable.html', {'form': form})


def output(request):
    form = GetTimeTableForm()
    return render(request, 'timetable/list.html',{'form': form})


def download(request):
    return render(request, 'timetable/download.html')


def return_results(chosen_grade, chosen_litera):
    try:
        my_grade = Grades.objects.get(number=chosen_grade, letter=chosen_litera)
    except ObjectDoesNotExist:
        my_grade = Grades.objects.create(number=chosen_grade, letter=chosen_litera)
        my_grade.save()
    lessons = Lessons.objects.filter(connection=my_grade).order_by('day', 'number')
    return lessons


def aj(request):
    CURRENT_DAY = time.localtime().tm_wday + 1
    current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
    next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
    g = request.GET.get("g")
    l = request.GET.get("l")
    l = unquote(l)
    my_grade = Grades.objects.get(number=g, letter=l)
    all_lessons = Lessons.objects.filter(connection=my_grade.id)
    week = {}
    today_lessons = all_lessons.filter(day=current_day_name)
    tomorrow_lessons = all_lessons.filter(day=next_day_name)
    today = []
    for les in today_lessons:
        today.append({
            "num": les.number.n,
            "sub": les.subject,
            "cls": les.classroom,
            "strt": str(les.number.start)[:-3],
            "end": str(les.number.end)[:-3]
        })
    week['Сегодня ({0})'.format(current_day_name)] = today
    tomorrow = []
    for les in tomorrow_lessons:
        tomorrow.append({
            "num": les.number.n,
            "sub": les.subject,
            "cls": les.classroom,
            "strt": str(les.number.start)[:-3],
            "end": str(les.number.end)[:-3]
        })
    week['Завтра ({0})'.format(next_day_name)] = tomorrow
    DAYWEEK_NAMES_list = list(DAYWEEK_NAMES.values())
    for weekday in DAYWEEK_NAMES_list[:-1]:
            week_les = all_lessons.filter(day=weekday)
            week_list = []
            for les in week_les:
                week_list.append({
                    "num": les.number.n,
                    "sub": les.subject,
                    "cls": les.classroom,
                    "strt": str(les.number.start)[:-3],
                    "end": str(les.number.end)[:-3]
                })
            week[weekday] = week_list
    week_json = json.dumps(week)
    return HttpResponse(week_json)
