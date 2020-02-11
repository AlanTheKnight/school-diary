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
    """Shows the timetable depending on the url."""
    CURRENT_DAY = time.localtime().tm_wday + 1
    # If current day isn't sunday, users will see timetable for today.
    if CURRENT_DAY != 7: current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
    # If surrent day isn't friday, users will see timetable for tomorrow.
    if CURRENT_DAY != 6: next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
    try:
        class_number = int(grade)
        class_letter = litera
        my_class = str(class_number) + class_letter
        my_grade = Grades.objects.get(number=class_number, letter=class_letter)
        if CURRENT_DAY != 7: lessons_list_today = Lessons.objects.filter(connection=my_grade.id, day=current_day_name)
        else: lessons_list_today = []
        if CURRENT_DAY != 6: lessons_list_tomorrow = Lessons.objects.filter(connection=my_grade.id, day=next_day_name)
        else: lessons_list_tomorrow = []
        lessons_list_monday = Lessons.objects.filter(connection=my_grade.id, day="Понедельник")
        lessons_list_tuesday = Lessons.objects.filter(connection=my_grade.id, day="Вторник")
        lessons_list_wednesday = Lessons.objects.filter(connection=my_grade.id, day="Среда")
        lessons_list_thursday = Lessons.objects.filter(connection=my_grade.id, day="Четверг")
        lessons_list_friday = Lessons.objects.filter(connection=my_grade.id, day="Пятница")
        lessons_list_saturday = Lessons.objects.filter(connection=my_grade.id, day="Суббота")
        return render(request, 'timetable/list.html', {
            'current_weekday': current_day_name,
            'today': lessons_list_today,
            'tomorrow': lessons_list_tomorrow,
            'my_grade': my_class,
            'monday': lessons_list_monday,
            'tuesday': lessons_list_tuesday,
            'wednesday': lessons_list_wednesday,
            'thursday': lessons_list_thursday,
            'friday': lessons_list_friday,
            'saturday': lessons_list_saturday})
    except Exception as error:
        return render(request, 'error.html', {
            'error': "404", 
            'title': "Расписание не найдено", 
            "description": "Класс отсутствует а базе данных. Попросите администратора добавить ваш класс."
        })


def download(request):
    return render(request, 'timetable/download.html')


@login_required(login_url='/diary/login/')
@admin_only
def dashboard(request):
    if request.method == "POST":
        form = GetTimeTableForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_litera = form.cleaned_data['litera']
            try:
                my_grade = Grades.objects.get(number=chosen_grade, letter=chosen_litera)
            except ObjectDoesNotExist:
                my_grade = Grades.objects.create(number=chosen_grade, letter=chosen_litera)
                my_grade.save()
            lessons = Lessons.objects.filter(connection=my_grade)
            return render(request, 'timetable/dashboard.html', {'form':form, 'lessons':lessons})
        
    form = GetTimeTableForm()
    return render(request, 'timetable/dashboard.html', {'form':form})


@login_required(login_url="/diary/login/")
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


@login_required(login_url="/diary/login/")
@admin_only
def create_lesson(request):
    if request.method == "POST":
        form = LessonCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
    form = LessonCreateForm()
    return render(request, 'timetable/create.html', {'form':form})


@login_required(login_url="/diary/login/")
@admin_only
def delete_lesson(request, id):
    lesson = Lessons.objects.get(id=id)
    if request.method == "POST":
        lesson.delete()
        return redirect('/timetable/dashboard')
    context = {'item':lesson}
    return render(request, 'timetable/lesson_delete.html', context)