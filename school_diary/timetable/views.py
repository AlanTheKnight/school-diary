from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from urllib.parse import unquote
from .forms import GetTimeTableForm, LessonCreateForm
from django.http import HttpResponseRedirect
from .models import Grades, Lessons
import time
from .decorators import admin_only
from django.core.exceptions import ObjectDoesNotExist


DAYWEEK_NAMES = {
    1:"Понедельник",
    2:"Вторник",
    3:"Среда",
    4:"Четверг",
    5:"Пятница",
    6:"Суббота",
    7:"Воскресенье"
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


def output(request, grade, litera):
    data = {}
    """Shows the timetable depending on the url."""
    CURRENT_DAY = time.localtime().tm_wday + 1
    # If current day isn't sunday, users will see timetable for today.
    current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
    # If surrent day isn't friday, users will see timetable for tomorrow.
    if CURRENT_DAY != 6: next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
    try:
        class_number = int(grade)
        class_letter = litera
        my_class = str(class_number) + class_letter
        my_grade = Grades.objects.get(number=class_number, letter=class_letter)
        all_lessons = Lessons.objects.filter(connection=my_grade.id)
        if CURRENT_DAY != 7: data["today"] = all_lessons.filter(day=current_day_name)
        else: data["today"] = []
        if CURRENT_DAY != 6: data["tomorrow"] = all_lessons.filter(day=next_day_name)
        else: data["tomorrow"] = []
        for weekday in DAYWEEK_NAMES.values():
            data[weekday] = all_lessons.filter(day=weekday)
        return render(request, 'timetable/list.html', {
            'current_weekday': current_day_name,
            'data':data,
            'my_grade': my_class})
    except Exception as error:
        print(error)
        return render(request, 'error.html', {
            'error': "404", 
            'title': "Расписание не найдено", 
            "description": "Расписание на этот класс еще не было добавлено администраторами.",
        })


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