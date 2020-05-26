from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from urllib.parse import unquote
from .forms import GetTimeTableForm, LessonCreateForm, BellCreateForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Grades, Lessons, BellsTimeTable
import time
import json
from .decorators import admin_only
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator



DAYWEEK_NAMES = {
    1:"Понедельник",
    2:"Вторник",
    3:"Среда",
    4:"Четверг",
    5:"Пятница",
    6:"Суббота",
    7:"Воскресенье"
}

SCHOOLS = dict([
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
])


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


@login_required(login_url='/login/')
@admin_only
def dashboard(request):
    if request.method == "POST":
        form = GetTimeTableForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_litera = form.cleaned_data['litera']
            request.session['tt_grade'] = chosen_grade
            request.session['tt_litera'] = chosen_litera
            lessons = return_results(chosen_grade, chosen_litera)
    else:
        if 'tt_grade' in request.session:
            chosen_grade = request.session['tt_grade']
            chosen_litera = request.session['tt_litera']
            lessons = return_results(chosen_grade, chosen_litera)
        else:
            lessons = []
            chosen_grade = ""
            chosen_litera = ""
        form = GetTimeTableForm()
        
    context = {
        'form':form,
        'lessons':lessons,
        'number':chosen_grade,
        'letter':chosen_litera
    }
    return render(request, 'timetable/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def edit_lesson(request, id):
    lesson = Lessons.objects.get(id=id)
    form = LessonCreateForm(instance=lesson)
    if request.method == "POST":
        form = LessonCreateForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
            
    return render(request, 'timetable/create.html', {'form':form})


@login_required(login_url="/login/")
@admin_only
def create_lesson(request):
    if request.method == "POST":
        form = LessonCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
    form = LessonCreateForm()
    return render(request, 'timetable/create.html', {'form':form})


@login_required(login_url="/login/")
@admin_only
def delete_lesson(request, id):
    lesson = Lessons.objects.get(id=id)
    if request.method == "POST":
        lesson.delete()
        return redirect('/timetable/dashboard')
    context = {'item':lesson}
    return render(request, 'timetable/lesson_delete.html', context)

"""
List of HTML pages are rendered by these functions:
- timetable/lesson_delete.html
    Page with lesson deleting confirmation.
- timetable/create.html
    Page where admin creates a new lesson.
- timetable/dashboard.html
    Page where admins can edit lessons.
- timetable/download.html
    Page with links to timetable download.
- timetable/list.html
    Page where timetable is displayed.
- timetable/timetable.html
    Page with class selection.
"""

@login_required(login_url="/login/")
@admin_only
def bells_dashboard_first_page(request):
    return redirect('/timetable/bells/dashboard/1')


@login_required(login_url="/login/")
@admin_only
def bells_dashboard(request, page):
    objects = BellsTimeTable.objects.all() # Replace Model
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
    return render(request, 'bells/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def bells_delete(request, pk):
    obj = BellsTimeTable.objects.get(pk=pk) # Replace model
    if request.method == "POST":
        obj.delete()
        return redirect('bells_dashboard')
    context = {
        "object": obj,
        "help_text": "Вы уверены, что хотите удалить эту запись?"
    }
    return render(request, 'bells/delete.html', context)


@login_required(login_url="/login/")
@admin_only
def bells_update(request, pk):
    obj = BellsTimeTable.objects.get(pk=pk) # Replace Model
    if request.method == "POST":
        form = BellCreateForm(request.POST, instance=obj) # Replace SomeForm
        if form.is_valid():
            form.save()
            return redirect('bells_dashboard')
    form = BellCreateForm(instance=obj) # Replace SomeForm
    return render(request, 'bells/create.html', {'form': form, 'title':"Добавить звонок"})


@login_required(login_url="/login/")
@admin_only
def bells_create(request): # Replace Model
    if request.method == "POST":
        form = BellCreateForm(request.POST) # Replace SomeForm
        if form.is_valid():
            form.save()
            return redirect('bells_dashboard')
    form = BellCreateForm() # Replace SomeForm
    return render(request, 'bells/create.html', {'form': form, 'title':"Добавить звонок"})

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