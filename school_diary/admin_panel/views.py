import xlsxwriter
import datetime
import os
from shutil import rmtree
from django.shortcuts import render, redirect
from diary.decorators import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.conf import settings

import diary.models as models
import diary.forms as forms
from .forms import ArticleCreationForm, BellCreateForm, LessonCreateForm
import news.models as news_models
from timetable.forms import GetTimeTableForm
import timetable.models as tt_models


@admin_only
def admin_panel(request):
    return render(request, 'admin_panel.html')


# Students dashboard ==========================================================


@login_required(login_url="/login/")
@admin_only
def students_dashboard_first_page(request):
    return redirect('students_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def students_dashboard(request, page):
    """
    Send a dashboard with up to 100 students.
    TODO: Test a pagination.
    """
    students = models.Students.objects.all()
    classes = models.Grades.objects.all()
    if request.method == "POST":
        fn = request.POST.get('first_name')
        s = request.POST.get('surname')
        email = request.POST.get('email')
        s_class = int(request.POST.get('class'))
        if fn or s or email or s_class:
            if s_class == -2:
                students = students.filter(
                    first_name__icontains=fn,
                    surname__icontains=s,
                    account__email__icontains=email)
            elif s_class == -1:
                students = students.filter(
                    first_name__icontains=fn,
                    surname__icontains=s,
                    account__email__icontains=email,
                    grade=None)
            else:
                students = students.filter(
                    first_name__icontains=fn, surname__icontains=s,
                    account__email__icontains=email, grade__id=s_class)
    students = Paginator(students, 100)
    students = students.get_page(page)
    context = {'students': students, 'classes': classes}
    return render(request, 'students/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def students_delete(request, id):
    """
    Delete a student.
    """
    u = models.Users.objects.get(email=id)
    s = models.Students.objects.get(account=u)
    if request.method == "POST":
        u.delete()
        s.delete()
        return redirect('students_dashboard')
    return render(request, 'students/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def students_update(request, id):
    """
    Edit student's account info.
    """
    u = models.Users.objects.get(email=id)
    s = models.Students.objects.get(account=u)
    if request.method == "POST":
        form = forms.StudentEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('students_dashboard')
    form = forms.StudentEditForm(instance=s)
    return render(request, 'students/update.html', {'form': form})


# Administrators dashboard ====================================================


@login_required(login_url="/login/")
@admin_only
def admins_dashboard_first_page(request):
    """
    Redirect user to the first page of admin dashboard.
    """
    return redirect('admins_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def admins_dashboard(request, page):
    """
    Send dashboard with up to 100 administrators
    """
    u = models.Administrators.objects.all()
    u = Paginator(u, 100)
    u = u.get_page(page)
    return render(request, 'admins/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def admins_delete(request, id):
    """
    Delete an admin.
    """
    u = models.Users.objects.get(email=id)
    s = models.Administrators.objects.get(account=u)
    if request.method == "POST":
        u.delete()
        s.delete()
        return redirect('admins_dashboard')
    return render(request, 'admins/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def admins_update(request, id):
    """
    Edit admin's info.
    """
    u = models.Users.objects.get(email=id)
    s = models.Administrators.objects.get(account=u)
    if request.method == "POST":
        form = forms.AdminsEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('admins_dashboard')
    form = forms.AdminsEditForm(instance=s)
    return render(request, 'admins/update.html', {'form': form})


# Teachers dashboard ==========================================================


@login_required(login_url="/login/")
@admin_only
def teachers_dashboard_first_page(request):
    return redirect('teachers_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def teachers_dashboard(request, page):
    u = models.Teachers.objects.all()
    if request.method == "POST":
        fn = request.POST.get('first_name')
        s = request.POST.get('surname')
        email = request.POST.get('email')
        u = u.filter(
            first_name__icontains=fn, surname__icontains=s,
            account__email__icontains=email)
    u = Paginator(u, 50)
    u = u.get_page(page)
    return render(request, 'teachers/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def teachers_delete(request, id):
    """
    Delete a teacher.
    """
    u = models.Users.objects.get(email=id)
    s = models.Teachers.objects.get(account=u)
    if request.method == "POST":
        u.delete()
        s.delete()
        return redirect('teachers_dashboard')
    return render(request, 'teachers/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def teachers_update(request, id):
    """
    Edit teachers's account info.
    """
    u = models.Users.objects.get(email=id)
    s = models.Teachers.objects.get(account=u)
    if request.method == "POST":
        form = forms.TeacherEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('teachers_dashboard')
    form = forms.TeacherEditForm(instance=s)
    return render(request, 'teachers/update.html', {'form': form})


# Messages dashboard ==========================================================


@login_required(login_url="/login/")
@admin_only
def messages_dashboard_first_page(request):
    """Redirect a user to the first page of the dashboard."""
    return redirect('messages_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def messages_dashboard(request, page):
    u = models.AdminMessages.objects.all()
    u = Paginator(u, 100)
    u = u.get_page(page)
    return render(request, 'messages/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def messages_delete(request, pk):
    s = models.AdminMessages.objects.get(id=pk)
    if request.method == "POST":
        s.delete()
        return redirect('messages_dashboard')
    return render(request, 'messages/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def messages_view(request, pk):
    s = models.AdminMessages.objects.get(id=pk)
    return render(request, 'messages/view.html', {'s': s})


# Marks EXPORT section ========================================================
# Exporting TODO: move generated tables to MEDIA folder!!!


@login_required(login_url="/login/")
@admin_only
def generate_table(request, quarter):
    if settings.DEBUG:
        directory = os.path.join(settings.STATICFILES_DIRS[0], 'results')
    else:
        directory = os.path.join(settings.STATIC_ROOT, 'results')
    all_lessons = models.Lessons.objects.filter(quarter=quarter)
    all_grades = models.Grades.objects.all()
    all_marks = models.Marks.objects.filter(lesson__quarter=quarter)
    filename = str(datetime.datetime.now().strftime('%d.%m.%Y %I:%M:%S %p'))
    filename += '.xlsx'
    file = 'results/' + filename
    workbook = xlsxwriter.Workbook(os.path.join(directory, filename))
    row = 0
    for grade in all_grades:
        worksheet = workbook.add_worksheet(str(grade))
        lessons = all_lessons.filter(
            grade=grade).order_by('date', 'subject__name')
        for lesson in lessons:
            worksheet.write(row, 0, str(lesson.grade))
            worksheet.write(row, 1, lesson.date.strftime('%d.%m.%Y'))
            worksheet.write(row, 2, str(lesson.subject))
            worksheet.write(row, 3, lesson.theme)
            worksheet.write(row, 4, lesson.homework)
            marks = all_marks.filter(
                lesson=lesson).order_by('student__surname', 'student__name')
            row += 1
            for mark in marks:
                worksheet.write(row, 0, mark.student.surname)
                worksheet.write(row, 1, mark.student.first_name)
                worksheet.write(row, 2, mark.amount)
            row += 2
    workbook.close()
    context = {'filename': file}
    return render(request, 'download-sheet.html', context)


@login_required(login_url="/login/")
@admin_only
def empty_backup_folder(request):
    if settings.DEBUG:
        directory = os.path.join(settings.STATICFILES_DIRS[0], 'results')
    else:
        directory = os.path.join(settings.STATIC_ROOT, 'results')
    rmtree(directory)
    os.mkdir(directory)
    return redirect('export_marks')


@login_required(login_url="/login/")
@admin_only
def export_page(request):
    if request.method == "POST":
        quarter = request.POST.get('quarter')
        return redirect('export_marks_download', quarter=quarter)
    return render(request, 'export.html')


# NEWS PANEL ==================================================================


@login_required(login_url="/login/")
@admin_only
def news_create(request):
    """Page where admin can create a new post."""
    if request.method == "POST":
        form = ArticleCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_dashboard')
    else:
        form = ArticleCreationForm()
        return render(request, 'news/news_editor.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def news_dashboard(request, page):
    """Dashboard for posts."""
    news = news_models.Publications.objects.all()
    news = Paginator(news, 100)  # 100 posts per page
    news = news.get_page(page)
    return render(request, 'news/news_dashboard.html', {'news': news})


@login_required(login_url="/login/")
@admin_only
def news_dashboard_first_page(request):
    """Redirects user to the first page of the dashboard."""
    return redirect('news_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def news_delete(request, pk):
    """Page where admin deletes a post."""
    article = news_models.Publications.objects.get(id=pk)
    if request.method == "POST":
        article.delete()
        return redirect('/news/dashboard')
    context = {'item': article}
    return render(request, 'news/news_delete.html', context)


@login_required(login_url="/login/")
@admin_only
def news_update(request, pk):
    """Page where post can be edited."""
    article = news_models.Publications.objects.get(id=pk)
    form = ArticleCreationForm(instance=article)
    if request.method == 'POST':
        form = ArticleCreationForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            if request.POST.get('deleteimage') is not None:
                article.image = ''
                article.save()
            return redirect('news_dashboard')
    context = {'form': form, 'data': article}
    return render(request, 'news/news_editor.html', context)


# Timetable' lessons dashboard =====================================


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
    my_grade = tt_models.Grades.objects.get_or_create(number=chosen_grade, letter=chosen_litera)[0]
    lessons = tt_models.Lessons.objects.filter(connection=my_grade).order_by('day', 'number')
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
    lesson = tt_models.Lessons.objects.get(id=pk)
    form = LessonCreateForm(instance=lesson)
    if request.method == "POST":
        form = LessonCreateForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
    return render(request, 'timetable/create.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def tt_lesson_create(request):
    if request.method == "POST":
        form = LessonCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_dashboard')
    form = LessonCreateForm()
    return render(request, 'timetable/create.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def tt_lesson_delete(request, pk):
    lesson = tt_models.Lessons.objects.get(id=pk)
    if request.method == "POST":
        lesson.delete()
        return redirect('tmetable_dashboard')
    context = {'item': lesson}
    return render(request, 'timetable/delete.html', context)


# Bells dashboard =================================================


@login_required(login_url="/login/")
@admin_only
def bells_dashboard_first_page(request):
    return redirect('bells_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def bells_dashboard(request, page):
    objects = tt_models.BellsTimeTable.objects.all()
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
    obj = tt_models.BellsTimeTable.objects.get(pk=pk)
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
    obj = tt_models.BellsTimeTable.objects.get(pk=pk)
    if request.method == "POST":
        form = BellCreateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('bells_dashboard')
    form = BellCreateForm(instance=obj)
    return render(request, 'bells/create.html', {'form': form, 'title': "Добавить звонок"})


@login_required(login_url="/login/")
@admin_only
def bells_create(request):
    if request.method == "POST":
        form = BellCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bells_dashboard')
    form = BellCreateForm()
    return render(request, 'bells/create.html', {'form': form, 'title': "Добавить звонок"})
