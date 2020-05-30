from django.shortcuts import render, redirect
from diary.decorators import admin_only
from django.contrib.auth.decorators import login_required
from admin_panel import forms
from timetable.forms import GetTimeTableForm
from timetable import models


SCHOOLS = dict([
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
])


@login_required(login_url='/login/')
@admin_only
def tt_dashboard(request):
    if request.method == "POST":
        form = GetTimeTableForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_litera = form.cleaned_data['litera']
            request.session['tt_grade'] = chosen_grade
            request.session['tt_litera'] = chosen_litera
        return redirect('timetable_dashboard')
    if 'tt_grade' in request.session:
        chosen_grade = request.session['tt_grade']
        chosen_litera = request.session['tt_litera']
    else:
        chosen_grade = '1'
        chosen_litera = 'А'
    form = GetTimeTableForm(initial={
        'grade': chosen_grade,
        'litera': chosen_litera
    })
    my_grade = models.Grades.objects.get_or_create(number=chosen_grade, letter=chosen_litera)[0]
    lessons = models.Lessons.objects.filter(connection=my_grade).order_by('day', 'number')
    context = {
        'form': form,
        'lessons': lessons,
        'number': chosen_grade,
        'letter': chosen_litera
    }
    return render(request, 'timetable/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def tt_lesson_update(request, pk):
    lesson = models.Lessons.objects.get(id=pk)
    form = forms.LessonCreateForm(instance=lesson)
    if request.method == "POST":
        form = forms.LessonCreateForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
    return render(request, 'timetable/create.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def tt_lesson_create(request):
    if request.method == "POST":
        form = forms.LessonCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
    form = forms.LessonCreateForm()
    return render(request, 'timetable/create.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def tt_lesson_delete(request, pk):
    lesson = models.Lessons.objects.get(id=pk)
    if request.method == "POST":
        lesson.delete()
        return redirect('tmetable_dashboard')
    context = {'item': lesson}
    return render(request, 'timetable/delete.html', context)
