import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import http
from diary.decorators import student_only
from diary import forms
from diary import homework
from diary import models
import utils
from .forms import HomeworkForm


MESSAGES = {
    'NO_GRADE': {
        'message': ("Вы не состоите в классе. Попросите Вашего"
                    "классного руководителя добавить Вас в класс.")
    },
    'NOT_SPECIAL': {
        'message': ("Вы не староста класса.")
    }
}


def is_special(function):
    def wrapper(request, *args, **kwargs):
        if request.user.student.special:
            return function(request, *args, **kwargs)
        return render(request, 'access_denied.html', MESSAGES['NOT_SPECIAL'])
    return wrapper


def in_grade(function):
    def wrapper(request, *args, **kwargs):
        if request.user.student.grade is not None:
            return function(request, *args, **kwargs)
        return render(request, 'access_denied.html', MESSAGES['NO_GRADE'])
    return wrapper


@login_required(login_url="login")
@student_only
@in_grade
def show_homework(request):
    """
    Page where students can see their homework.
    """
    student = request.user.student
    grade = student.grade
    if "date" in request.GET:
        form = forms.DatePickForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            lessons = homework.get_homework(grade, start_date=date)
            context = {'form': form, 'lessons': lessons, 'date': date}
            return render(request, 'homework/homework.html', context)
    start_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=7)
    lessons = homework.get_homework(grade, start_date=start_date, end_date=end_date)
    form = forms.DatePickForm()
    return render(request, 'homework/homework.html', {'form': form, 'lessons': lessons})


@student_only
@is_special
@in_grade
def homework_list(request, quarter=utils.get_default_quarter()):
    if not (1 <= quarter <= 4):
        raise http.Http404
    if "quarter" in request.GET:
        return redirect('homework-list', int(request.GET.get("quarter")))
    termform = forms.QuarterSelectionForm(initial={
        'quarter': quarter
    })
    subjects = request.user.student.grade.subjects.all()
    hw_form = HomeworkForm(subjects)
    if request.method == "POST":
        hw_form = HomeworkForm(subjects, request.POST, request.FILES)
        if hw_form.is_valid():
            hw_form.add_homework(request.user.student.grade)
            hw_form = HomeworkForm(subjects)
    lessons = homework.get_homework(request.user.student.grade, quarter=quarter, reverse=True)
    return render(request, 'homework/list.html', {
        'termform': termform, 'lessons': lessons, 'form': hw_form
    })


@student_only
@is_special
@in_grade
def homework_delete(request, pk: int):
    lesson = models.Lessons.objects.get(id=pk)
    if request.method == "POST":
        lesson.delete()
        return redirect('homework-list')
    return render(request, 'homework/delete.html', {'lesson': lesson})


@student_only
@is_special
@in_grade
def homework_edit(request, pk: int):
    subjects = request.user.student.grade.subjects.all()
    lesson = models.Lessons.objects.get(id=pk)
    if request.method == "POST":
        form = HomeworkForm(subjects, request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('homework-list')
    else:
        form = HomeworkForm(subjects, instance=lesson)
    return render(request, 'homework/edit.html', {'form': form})
