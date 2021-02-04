import xlsxwriter
import datetime
import os
from shutil import rmtree
from django.shortcuts import render, redirect
from core.access import admin_only
from django.contrib.auth.decorators import login_required
from django.conf import settings
from core import models


# TODO(ideasoft-spb@yandex.com): move generated tables to MEDIA folder!!!
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
