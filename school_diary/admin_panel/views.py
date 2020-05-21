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


# Students dashboard


@login_required(login_url="/login/")
@admin_only
def students_dashboard_first_page(request):
    return redirect('/students/dashboard/1')


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


# Administrators dashboard


@login_required(login_url="/login/")
@admin_only
def admins_dashboard_first_page(request):
    """
    Redirect user to the first page of admin dashboard.
    """
    return redirect('/admins/dashboard/1')


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


# Teachers dashboard


@login_required(login_url="/login/")
@admin_only
def teachers_dashboard_first_page(request):
    return redirect('/teachers/dashboard/1')


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


# Messages dashboard


@login_required(login_url="/login/")
@admin_only
def messages_dashboard_first_page(request):
    """Redirect a user to the first page of the dashboard."""
    return redirect('/messages/dashboard/1')


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
    return redirect('export')


@login_required(login_url="/login/")
@admin_only
def export_page(request):
    if request.method == "POST":
        quarter = request.POST.get('quarter')
        return redirect('/export/{}'.format(quarter))
    return render(request, 'export.html')
