import datetime
from functools import reduce
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from . import forms
from .decorators import (
    unauthenticated_user, admin_only, allowed_users,
    teacher_only, student_only)
from . import models
from .functions import *


@unauthenticated_user
def user_register(request):
    """
    New student registration.
    """
    if request.method == 'POST':
        form = forms.StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Учётная запись была создана успешно.")
            return redirect('/login')
    if request.POST:
        form = forms.StudentSignUpForm(request.POST)
    else:
        form = forms.StudentSignUpForm()
    return render(request, 'registration.html', {'form': form, 'error': 0})


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(
                request, 'Неправильный адрес электронной почты или пароль.')
    form = forms.UsersLogin()
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="/login/")
def user_profile(request):
    """
    User profile page (diary56.ru/profile/)
    """
    if request.user.account_type == 0:
        data = models.Users.objects.get(email=request.user)
    if request.user.account_type == 1:
        data = models.Administrators.objects.get(account=request.user)
    if request.user.account_type == 2:
        data = models.Teachers.objects.get(account=request.user)
        if request.method == "POST":
            if 'image-upload' in request.POST:
                data.avatar = request.FILES.get('avatar')
                data.save()
            elif 'image-delete' in request.POST:
                data.avatar.delete()
    if request.user.account_type == 3:
        data = models.Students.objects.get(account=request.user)
    context = {'data': data}
    return render(request, 'profile.html', context)


@login_required(login_url="/login/")
@admin_only
def admin_register(request):
    if request.method == 'POST':
        form = forms.AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Новый аккаунт администратора был создан успешно.")
            return redirect('/login/')
    if request.POST:
        form = forms.AdminSignUpForm(request.POST)
    else:
        form = forms.AdminSignUpForm()
    context = {'form': form, 'error': 0}
    return render(request, 'registration_admin.html', context)


@login_required(login_url="/login/")
@admin_only
def teacher_register(request):
    if request.method == 'POST':
        form = forms.TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Новый аккаунт учителя был создан успешно.")
            return redirect('/login/')
    if request.POST:
        form = forms.TeacherSignUpForm(request.POST)
    else:
        form = forms.TeacherSignUpForm()
    context = {'form': form, 'error': 0}
    return render(request, 'registration_teacher.html', context)


@teacher_only
@login_required(login_url="/login/")
@transaction.atomic
def lesson_page(request, pk):
    lesson = models.Lessons.objects.get(pk=pk)

    context = {
        'lesson': lesson,
    }
    context.update(create_controls(grade=models.Grades.objects.get(
        pk=request.session['grade']),
        subject=models.Subjects.objects.get(
            pk=request.session['subject']), term=request.session['term']
        )
    )
    if request.method == 'POST':
        lesson = models.Lessons.objects.get(pk=request.POST.get('pk'))
        if request.FILES.get('h_file'):
            lesson.h_file = request.FILES.get('h_file')
        lesson.date = request.POST.get('date')
        lesson.quarter = get_quarter_by_date(lesson.date)
        lesson.theme = request.POST.get('theme')
        lesson.control = models.Controls.objects.get(
            pk=request.POST.get('control'))
        lesson.homework = request.POST.get('homework')
        if request.POST.get('deletehwfile') is not None:
            lesson.h_file = ""
        lesson.save()
        return redirect('diary')

    return render(request, 'lesson_page.html', context)


@login_required(login_url='/login/')
@teacher_only
def delete_lesson(request, pk):
    lesson = models.Lessons.objects.get(pk=pk)
    if request.method == "POST":
        lesson.delete()
        return redirect('diary')
    return render(request, 'lesson_delete.html', {'item': lesson})


def students_diary(request):
    student = models.Students.objects.get(account=request.user)
    grade = student.grade
    if grade is None:
        return render(request, 'access_denied.html', {'message': "Вы не состоите в классе.\
        Попросите Вашего классного руководителя добавить Вас в класс."})
    if 'selected' in request.POST:
        subject = request.POST.get('subject')
        return redirect('/diary/{}'.format(subject))
    elif 'all' in request.POST:
        chosen_quarter = int(request.POST.get('term'))
        subjects = grade.subjects.all()
        all_marks = student.marks_set.filter(lesson__quarter=chosen_quarter)
        if not all_marks:
            return render(request, 'no_marks.html')
        d = {}
        max_length, total_missed = 0, 0

        for s in subjects:
            marks = all_marks.filter(subject=s.id).order_by('lesson__date')
            if len(marks) > max_length:
                max_length = len(marks)

            n_amount = 0
            marks_list = []
            for i in marks:
                if i.lesson.control.weight != 100:
                    if i.amount != -1:
                        marks_list.append(i)
                    else:
                        n_amount += 1
            avg = get_average(marks_list)
            smart_avg = get_smart_average(marks_list)
            d.update({s: [avg, smart_avg, marks]})

            total_missed += n_amount

        for subject in d:
            d[subject].append(range(max_length - len(d[subject][2])))

        context = {
            'student': student,
            'd': d,
            'max_length': max_length,
            'total_missed': total_missed,
            'term': chosen_quarter,
        }
        return render(request, 'marklist.html', context)

    subjects = grade.subjects.all()
    context = {'subjects': subjects}
    return render(request, 'diary_student.html', context)


def teachers_diary(request):
    teacher = models.Teachers.objects.get(account=request.user)
    context = {'Teacher': teacher,
               'subjects': teacher.subjects.all(),
               'grades': models.Grades.objects.filter(teachers=teacher),
               # 'controls': controls
               }

    if request.method == 'POST':
        # If teacher filled in a form with name = 'getgrade' then
        # build a table with marks for all students and render it.
        if 'getgrade' in request.POST:
            subject = models.Subjects.objects.get(name=request.POST.get('subject'))
            grade = request.POST.get('grade')
            request.session['subject'] = subject.id
            term = int(request.POST.get('term'))
            request.session['term'] = int(term)
            number = int(grade[0:-1])
            letter = grade[-1]
            try:
                grade = models.Grades.objects.get(number=number, subjects=subject, letter=letter, teachers=teacher)
                request.session['grade'] = grade.id
            except ObjectDoesNotExist:
                messages.error(request, 'Ошибка')
                return render(request, 'teacher.html', context)
            context.update(create_table(grade, subject, term))

            context.update(create_controls(grade=grade, subject=subject, term=term))
            return render(request, 'teacher.html', context)

        elif 'createlesson' in request.POST:
            date = request.POST.get('date')
            quarter = get_quarter_by_date(date)
            theme = request.POST.get('theme')
            homework = request.POST.get('homework')
            control = models.Controls.objects.get(id=request.POST.get('control'))
            grade = models.Grades.objects.get(id=request.session['grade'])
            subject = models.Subjects.objects.get(id=request.session['subject'])
            term = request.session['term']
            h_file = request.FILES.get('h_file')
            lesson = models.Lessons.objects.create(
                date=date, h_file=h_file, quarter=quarter,
                theme=theme, homework=homework,
                control=control, grade=grade, subject=subject)
            lesson.save()
            context.update(create_table(grade=grade, subject=subject, quarter=term))
            context.update(create_controls(grade=grade, subject=subject, term=term))
            return render(request, 'teacher.html', context)

        elif 'addcomment' in request.POST:
            # Get data from session
            grade = models.Grades.objects.get(id=request.session['grade'])
            term = request.session['term']
            subject = models.Subjects.objects.get(id=request.session['subject'])
            comment = request.POST.get('comment')
            data = request.POST.get('commentdata')
            student_id = data.split("|")[0]
            lesson_id = data.split("|")[1]
            student = models.Students.objects.get(account=student_id)
            lesson = models.Lessons.objects.get(id=lesson_id)
            mark = models.Marks.objects.get(student=student, lesson=lesson)
            mark.comment = comment
            mark.save()
            context.update(create_table(grade=grade, subject=subject, quarter=term))
            context.update(create_controls(grade=grade, subject=subject, term=term))
            return render(request, 'teacher.html', context)
        else:
            # Save marks block
            marks_dict = {
                tuple(map(int, k.replace("mark_", "").split("|"))): str(request.POST[k])
                for k in dict(request.POST)
                if k.startswith('mark_')
            }
            subject = models.Subjects.objects.get(id=request.POST.get('subject_id'))

            marks_raw = models.Marks.objects.select_for_update().filter(
                student__grade_id=request.POST.get('grade_id'),
                lesson__grade_id=request.POST.get('grade_id'),
                lesson__subject_id=subject.id
            )

            marks_in_db = {
                (x.student_id, x.lesson_id): x
                for x in marks_raw
            }

            objs_for_update = []
            for k, v in marks_dict.items():
                if v != "" and k in marks_in_db.keys() and marks_in_db[k].amount != int(v):
                    marks_in_db[k].amount = int(v)
                    objs_for_update.append(marks_in_db[k])

            objs_for_create = [
                models.Marks(lesson_id=k[1], student_id=k[0], amount=int(v), subject=subject)
                for k, v in marks_dict.items()
                if v != "" and k not in marks_in_db.keys()
            ]

            objs_for_remove = [
                Q(id=marks_in_db[k].id)
                for k, v in marks_dict.items()
                if v == "" and k in marks_in_db
            ]
            models.Marks.objects.bulk_update(objs_for_update, ['amount'])

            models.Marks.objects.bulk_create(objs_for_create)

            if len(objs_for_remove) != 0:
                models.Marks.objects.filter(reduce(lambda a, b: a | b, objs_for_remove)).delete()

            context.update(create_table(grade=models.Grades.objects.get(pk=request.session['grade']), subject=subject,
                                        quarter=request.session['term']))
            context.update(
                create_controls(grade=models.Grades.objects.get(pk=request.session['grade']), subject=subject,
                                term=request.session['term']))
            return render(request, 'teacher.html', context)
    else:
        return render(request, 'teacher.html', context)

      
@login_required(login_url="/login/")
def diary(request):
    """
    Main function for displaying diary pages to admins/teachers/students.
    """

    # If user is admin
    if request.user.account_type == 0 or request.user.account_type == 1:
        return render(request, 'diary_admin_main.html')

    # If user is student
    elif request.user.account_type == 3:
        students_diary(request)

    # If user is teacher
    elif request.user.account_type == 2:
        teachers_diary(request)
    else:
        redirect('/')


@login_required(login_url="login")
@allowed_users(allowed_roles=['students'], message="Доступ к этой странице имеют только ученики.")
def stats(request, id, term):
    student = models.Students.objects.get(account=request.user)
    grade = student.grade
    if grade is None:
        return render(request, 'access_denied.html', {'message': "Вы не состоите в классе.\
            Попросите Вашего классного руководителя добавить Вас в класс."})
    try:
        subject = models.Subjects.objects.get(id=id)
    except ObjectDoesNotExist:
        context = {
            'title': 'Мы не можем найти то, что Вы ищите.',
            'error': '404',
            'description': 'Данный предмет отстуствует.'
        }
        return render(request, 'error.html', context)
    lessons = models.Lessons.objects.filter(grade=grade, subject=subject, quarter=term)
    marks = []
    marks = student.marks_set.filter(subject=subject, lesson__quarter=term)

    # If student has no marks than send him a page with info.
    # Otherwise, student will get a page with statistics and his results.
    if marks:
        n_amount = 0
        marks_list = []
        for i in marks:
            if i.amount != -1:
                if i.lesson.control.weight == 100:
                    continue
                marks_list.append(i)
            else:
                n_amount += 1

        avg = get_average(marks_list)
        smart_avg = get_smart_average(marks_list)

        marks_amounts = [i.amount for i in marks if i.amount != -1 and i.lesson.control.weight != 100]
        data = []
        for i in range(5, 1, -1):
            data.append(marks_amounts.count(i))
        data.append(n_amount)

        needed, needed_mark = 0, 0
        if avg[0] <= 4.5:
            needed = 9 * avg[2] - 2 * avg[1] + 1
            needed_mark = 5
        if avg[0] <= 3.5:
            needed = (7 * avg[2] - 2 * avg[1]) // 3 + 1
            needed_mark = 4
        if avg[0] <= 2.5:
            needed = (5 * avg[2] - 2 * avg[1]) // 5 + 1
            needed_mark = 3

        context = {
            'term': term,
            'lessons': lessons,
            'marks': marks,
            'subject': subject,
            'data': data,
            'avg': avg,
            'smartavg': smart_avg,
            'needed': needed,
            'needed_mark': needed_mark}
        return render(request, 'results.html', context)
    return render(request, 'no_marks.html')


@login_required(login_url="login")
@student_only
def homework(request):
    student = models.Students.objects.get(account=request.user)
    grade = student.grade
    if grade is None:
        return render(request, 'access_denied.html', {'message': """Вы не состоите в классе, попросите Вашего
        классного руководителя Вас добавить"""})
    if request.method == "POST":
        if "day" in request.POST:
            form = forms.DatePickForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                raw_lessons = models.Lessons.objects.filter(date=date, grade=grade)
                lessons = []
                for lesson in raw_lessons:
                    if lesson.homework or lesson.h_file:
                        lessons.append(lesson)
            return render(request, 'homework.html', {'form': form, 'lessons': lessons, 'date': date})
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=6)
    lessons = models.Lessons.objects.filter(date__range=[start_date, end_date], grade=grade, homework__iregex=r'\S+')
    if not lessons:
        lessons = models.Lessons.objects.filter(date__range=[start_date, end_date], grade=grade, h_file__iregex=r'\S+')
    form = forms.DatePickForm()
    return render(request, 'homework.html', {'form': form, 'lessons': lessons})


@login_required(login_url="login")
@teacher_only
def add_student_page(request):
    """
    Page where teachers can add students to their grade.
    """
    try:
        grade = models.Grades.objects.get(main_teacher=request.user.id)
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': "Вы не классный руководитель."})
    students = models.Students.objects.filter(grade=grade)

    if request.method == "POST":
        form = forms.AddStudentToGradeForm(request.POST)
        if form.is_valid:
            email = request.POST.get('email')
            fn = request.POST.get('first_name').strip()
            s = request.POST.get('surname').strip()
            if fn or s or email:
                search = models.Students.objects.filter(
                    first_name__icontains=fn, surname__icontains=s,
                    account__email__icontains=email)
            else:
                search = []
            context = {
                'form': form, 'search': search,
                'grade': grade, 'students': students
            }
            return render(request, 'grades/add_student.html', context)

    form = forms.AddStudentToGradeForm()
    context = {'form': form, 'grade': grade, 'students': students}
    return render(request, 'grades/add_student.html', context)


@login_required(login_url="login")
@teacher_only
def add_student(request, i):
    """
    Function defining the process of adding new student to a grade and confirming it.
    """
    u = models.Users.objects.get(email=i)
    s = models.Students.objects.get(account=u)
    if request.method == "POST":
        try:
            grade = models.Grades.objects.get(main_teacher=request.user.id)
            s.grade = grade
            s.save()
            return redirect('add_student_page')
        except ObjectDoesNotExist:
            context = {'message': "Вы не классный руководитель."}
            return render(request, 'access_denied.html', context)
    else:
        return render(request, 'grades/add_student_confirm.html', {'s': s})


@login_required(login_url="login")
@teacher_only
def create_grade_page(request):
    if request.method == "POST":
        form = forms.GradeCreationForm(request.POST)
        if form.is_valid():
            grade = form.save()
            mt = models.Teachers.objects.get(account=request.user)
            grade.main_teacher = mt
            grade.save()
            return redirect('my_grade')
    form = forms.GradeCreationForm()
    context = {'form': form}
    return render(request, 'grades/add_grade.html', context)


@login_required(login_url="login")
@teacher_only
def my_grade(request):
    """
    Page with information about teacher's grade.
    """
    me = models.Teachers.objects.get(account=request.user)
    try:
        grade = models.Grades.objects.get(main_teacher=me)
    except ObjectDoesNotExist:
        grade = None
    context = {'grade': grade}
    return render(request, 'grades/my_grade.html', context)


def view_students_marks(request):
    me = models.Teachers.objects.get(account=request.user)
    if request.method == "POST":
        term = int(request.POST.get('term'))
    else:
        term = get_quarter_by_date(str(datetime.date.today()))

    try:
        grade = models.Grades.objects.get(main_teacher=me)
        students = models.Students.objects.filter(grade=grade)
        context = {
            'students': students,
            'term': term,
        }
        return render(request, 'grades/grade_marks.html', context)
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': 'Вы не являетесь классным руководителем.'})


def get_class_or_access_denied(request, teacher):
    try:
        my_class = models.Grades.objects.get(main_teacher=teacher)
        return my_class
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': 'Вы не являетесь классным руководителем.'})


def students_marks(request, pk, term):
    student = models.Students.objects.get(account=pk)
    me = models.Teachers.objects.get(account=request.user)
    my_class = get_class_or_access_denied(request, me)

    subjects = my_class.subjects.all()
    all_marks = student.marks_set.filter(lesson__quarter=term)
    if not all_marks:
        return render(request, 'grades/no_marks.html')
    d = {}
    max_length, total_missed = 0, 0
    for s in subjects:
        marks = all_marks.filter(subject=s.id).order_by('lesson__date')

        if len(marks) > max_length:
            max_length = len(marks)

        n_amount = 0
        marks_list = []
        for i in marks:
            if i.amount != -1:
                marks_list.append(i)
            else:
                n_amount += 1

        avg = get_average(marks_list)
        smart_avg = get_smart_average(marks_list)
        d.update({s: [avg, smart_avg, marks]})
        total_missed += n_amount

    for subject in d:
        d[subject].append(range(max_length - len(d[subject][2])))
    context = {
        'student': student,
        'd': d,
        'max_length': max_length,
        'total_missed': total_missed
    }
    return render(request, 'view_marks.html', context)


@login_required(login_url="login")
@teacher_only
def delete_student(request, i):
    """
    Function defining the process of deleting a student from a grade and confirming it.
    """
    u = models.Users.objects.get(email=i)
    s = models.Students.objects.get(account=u)
    if request.method == "POST":
        try:
            s.grade = None
            s.save()
            return redirect('add_student_page')
        except ObjectDoesNotExist:
            context = {'message': "Вы не классный руководитель."}
            return render(request, 'access_denied.html', context)
    else:
        return render(request, 'grades/delete_student_confirm.html', {'s': s})


@teacher_only
@login_required(login_url="login")
def admin_message(request):
    """
    Send a message to an admin.
    """
    if request.method == "POST":
        form = forms.AdminMessageCreationForm(request.POST)
        if form.is_valid():
            m = form.save()
            m.sender = request.user
            m.save()
            return redirect('profile')
    form = forms.AdminMessageCreationForm()
    return render(request, 'admin_messages.html', {'form': form})


@login_required(login_url="login")
@teacher_only
def mygradesettings(request):
    me = models.Teachers.objects.get(account=request.user)
    try:
        grade = models.Grades.objects.get(main_teacher=me)
        if request.method == "POST":
            form = forms.ClassSettingsForm(request.POST, instance=grade)
            if form.is_valid():
                form.save()
                return redirect('my_grade')
        form = forms.ClassSettingsForm(instance=grade)
        return render(request, 'grades/class_settings.html', {'form': form})
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': 'Вы не классный руководитель.'})
