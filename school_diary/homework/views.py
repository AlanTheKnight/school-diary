import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import http
from core.access import student_only, in_klass, is_president
from core import forms, models, homework


@login_required(login_url="login")
@student_only
@in_klass
def show_homework(request):
    """
    Page where students can see their homework.
    """
    student = request.user.student
    klass = student.klass
    if "date" in request.GET:
        form = forms.DatePickForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            lessons = homework.get_homework(klass, start_date=date)
            context = {'form': form, 'lessons': lessons, 'date': date}
            return render(request, 'homework/homework.html', context)
    start_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=7)
    lessons = homework.get_homework(klass, start_date=start_date, end_date=end_date)
    form = forms.DatePickForm()
    return render(request, 'homework/homework.html', {'form': form, 'lessons': lessons})


@student_only
@is_president
@in_klass
def homework_list(request, quarter=None):
    if quarter is None:
        quarter = models.Quarters.get_default_quarter().number
    if not (1 <= quarter <= 4):
        raise http.Http404
    if "quarter" in request.GET:
        return redirect('homework-list', int(request.GET.get("quarter")))
    quarter_form = forms.QuarterSelectionForm(initial={
        'quarter': quarter
    })
    subjects = request.user.student.klass.subjects.all()
    hw_form = homework.PresidentHomeworkForm(subjects)
    if request.method == "POST":
        hw_form = homework.PresidentHomeworkForm(subjects, request.POST, request.FILES)
        if hw_form.is_valid():
            hw_form.add_homework(request.user.student.klass)
            hw_form = homework.PresidentHomeworkForm(subjects)
    lessons = homework.get_homework(request.user.student.klass, quarter=quarter, reverse=True)
    return render(request, 'homework/list.html', {
        'quarter_form': quarter_form, 'lessons': lessons, 'form': hw_form
    })


@student_only
@is_president
@in_klass
def homework_delete(request, pk: int):
    lesson = models.Lessons.objects.get(id=pk)
    if request.method == "POST":
        lesson.delete()
        return redirect('homework-list')
    return render(request, 'homework/delete.html', {'lesson': lesson})


@student_only
@is_president
@in_klass
def homework_edit(request, pk: int):
    subjects = request.user.student.klass.subjects.all()
    lesson = models.Lessons.objects.get(id=pk)
    form = homework.PresidentHomeworkForm(subjects, instance=lesson)
    if request.method == "POST":
        form = homework.PresidentHomeworkForm(subjects, request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('homework-list')
    return render(request, 'homework/edit.html', {'form': form})


@student_only
@in_klass
def stats(request, quarter=None):
    if quarter is None:
        quarter = models.Quarters.get_default_quarter().number
    if not (1 <= quarter <= 4):
        raise http.Http404
    if "quarter" in request.GET:
        return redirect('homework-stats', int(request.GET.get("quarter")))
    klass = request.user.student.klass
    groups = klass.groups_set.all()
    hw = homework.get_homework(klass=klass, quarter=quarter, convert=False)
    subjects, data = [], []
    for group in groups:
        subjects.append(group.subject.name)
        data.append(hw.filter(group=group).count())
    context = {'subjects': subjects, 'data': data, 'no_hw': len(hw) == 0}
    return render(request, 'homework/hw_stats.html', context)
