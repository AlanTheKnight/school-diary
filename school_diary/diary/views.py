from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from .forms import *
from .decorators import unauthenticated_user, admin_only, allowed_users
from .models import *
import datetime



@unauthenticated_user
def user_register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Учётная запись была создана успешно.")
            return redirect('/login')
    if request.POST:
        form = StudentSignUpForm(request.POST)
    else:
        form = StudentSignUpForm()
    return render(request, 'registration.html', {'form': form, 'error': 0})


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Неправильный адрес электронной почты или пароль.')
    form = UsersLogin()
    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="/login/")
def user_profile(request):
    if request.user.account_type == 0:
        data = Users.objects.get(email=request.user)
    if request.user.account_type == 1:
        data = Administrators.objects.get(account=request.user)
    if request.user.account_type == 2:
        data = Teachers.objects.get(account=request.user)
    if request.user.account_type == 3:
        data = Students.objects.get(account=request.user)
    context = {'data': data}
    return render(request, 'profile.html', context)


@login_required(login_url="/login/")
@admin_only
def admin_register(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый администратор был создан успешно.")
            return redirect('/login/')
    if request.POST:
        form = AdminSignUpForm(request.POST)
    else:
        form = AdminSignUpForm()
    return render(request, 'registration_admin.html', {'form': form, 'error': 0})


@login_required(login_url="/login/")
@admin_only
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый учитель был создан успешно.")
            return redirect('/login/')
    if request.POST:
        form = TeacherSignUpForm(request.POST)
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration_teacher.html', {'form': form, 'error': 0})


def create_table_of_results(students, lessons, marks):
    table = {}
    for student in students:
        s = {}
        for lesson in lessons:
            a = 0
            for mark in marks:
                if mark.lesson_id == lesson.pk:
                    s.update({lesson: mark})
                    a = 1
            if not a:
                s.update({lesson:None})
        table.update({student: s})
    print(table)
    return table


@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
@login_required(login_url="/login/")  # TODO fix bug
def lesson_page(request):
    pk = request.GET.get('pk')
    lesson = Lessons.objects.get(pk=pk)
    if request.method == 'POST':
        form = LessonEditForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/diary/')
        else:
            pass
    form = LessonEditForm(instance=lesson)
    context = {
        'lesson': lesson,
        'form': form
    }
    return render(request, 'lesson_page.html', context)


def get_averange(list):
    """
    In: list of marks (integers)
    Out: averange value
    """
    return round(sum(list) / len(list), 2)


def get_smart_averange(list):
    s = 0
    w = 0
    for i in list:
        weight = i.lesson.control.weight
        s += weight * i.amount
        w += weight
    return round(s / w, 2)


def delete_lesson(request):
    pk = request.GET.get('pk')
    l = Lessons.objects.get(pk=pk)
    l.delete()
    return redirect('diary')


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
        student = Students.objects.get(account=request.user)
        grade = student.grade
        if grade is None:
            return render(request, 'access_denied.html', {'message':"Вы не состоите в классе.\
            Попросите Вашего классного руководителя добавить вас в класс."})
        if 'selected' in request.POST:
            subject = request.POST.get('subject')
            return redirect('/diary/{}'.format(subject))
        elif 'all' in request.POST:
            subjects = grade.subjects.all()
            d = {}
            max_length = 0
            for s in subjects:
                #m = Marks.objects.filter(student=student, subject=s)
                marks = student.marks_set.filter(subject=s.id)
                if len(marks) > max_length:
                    max_length = len(marks)
                a, n_amount = 0, 0
                for mark in marks:
                    if mark.amount != -1:
                        a += mark.amount
                    else:
                        n_amount += 1
                if len(marks) != 0:
                    d.update({s:[round(a/(len(marks)-n_amount),2),marks]})
                else:
                    d.update({s:['-',[]]})

            for subject, marks in d.items():
                d.update({subject:[marks[0],marks[1],range(max_length-len(marks[1]))]})
            print(d.items())
            context = {
                'student': student,
                'd': d,
                'max_length':max_length

            }
            return render(request,'marklist.html',context)

        subjects = grade.subjects.all()
        context = {'subjects': subjects}
        return render(request, 'diary_student.html', context)

    # If user is teacher
    elif request.user.account_type == 2:
        teacher = Teachers.objects.get(account=request.user)
        controls = Controls.objects.all()
        context = {'Teacher': teacher,
                   'subjects': teacher.subjects.all(),
                   'grades': Grades.objects.filter(teachers=teacher),
                   'controls': controls
                   }

        if request.method == 'POST':
            # If teacher filled in a form with name = 'getgrade' then
            # build a table with marks for all students and render it.
            if 'getgrade' in request.POST:
                subject = Subjects.objects.get(name=request.POST.get('subject'))
                grade = request.POST.get('grade')
                request.session['subject'] = subject.id
                if len(grade) == 3:
                    number = int(grade[0:2])
                else:
                    number = int(grade[0])
                letter = grade[-1]
                try:
                    grade = Grades.objects.get(number=number, subjects=subject, letter=letter, teachers=teacher)
                    request.session['grade'] = grade.id
                except ObjectDoesNotExist:
                    messages.error(request, 'Ошибка')
                    return render(request, 'teacher.html', context)
                # lessons_list = Lessons.objects.filter(grade=grade, subject=subject)
                lessons = Lessons.objects.filter(grade=grade, subject=subject).select_related("control")
                students = Students.objects.filter(grade=grade)
                # Делаем запрос 1 раз
                marks = Marks.objects.raw("""
                    SELECT
                        diary_marks.*
                    FROM diary_marks, diary_lessons, diary_students
                    WHERE diary_marks.student_id = diary_students.account_id AND diary_marks.lesson_id = diary_lessons.id
                            AND diary_lessons.grade_id = %s
                            AND diary_students.grade_id = %s
                            AND diary_lessons.subject_id = %s
                    ORDER BY diary_marks.date
                """, params=[grade.id, grade.id, subject.id])
                scope = create_table_of_results(students=students, lessons=lessons, marks=marks)
                # Ошибка - student.marks_set.get(lesson=lesson) делает 1 запрос. Получется n*m запросов, хотя все marks можно вытащить за 1 запрос
                # for mark in marks:
                #     print(mark.date)
                #     if students[mark.student_id] not in scope:
                #         scope[students[mark.student_id]] = {}
                #     lesson = lessons[mark.lesson_id]
                #     scope[students[mark.student_id]].update({lesson: mark})
                #
                # for sk, student in students.items():
                #     for lk, lesson in lessons.items():
                #         if student not in scope:
                #             scope[student] = {}
                #         if lesson not in scope[student]:
                #             scope[student].update({lesson: None})

                context.update({
                    'is_post': True,
                    'lessons': lessons,
                    'scope': scope
                })
                return render(request, 'teacher.html', context)

            elif 'createlesson' in request.POST:
                date = request.POST.get('date')
                theme = request.POST.get('theme')
                homework = request.POST.get('homework')
                control = Controls.objects.get(id=request.POST.get('control'))
                grade = Grades.objects.get(id=request.session['grade'])
                subject = Subjects.objects.get(id=request.session['subject'])
                lesson = Lessons.objects.create(
                    date=date, theme=theme, homework=homework, control=control, grade=grade, subject=subject
                )
                lesson.save()
                return HttpResponseRedirect('/diary/')

            # GETTING MARKS FROM FORM AND SAVE THEM
            # TODO: Optimize this algorithm, because it's slow
            else:
                subject = Subjects.objects.get(id=request.session['subject'])
                # We make a dictionary from all data we send
                for i in dict(request.POST):
                    # Missing a csrf token
                    if i == 'csrfmiddlewaretoken':
                        continue

                    # Split them. We get a student (li[0]) and id of
                    # lesson (li[1])
                    li = i.split('|')
                    account_id = li[0]
                    id_les = li[1]

                    # Get a student by his/her email
                    student = Students.objects.get(account=account_id)

                    # Get a lesson by it's id
                    lesson = Lessons.objects.get(pk=id_les)
                    amount = str(request.POST[i])

                    # If we can get a mark then change it, otherwise create a new one
                    try:
                        mark = Marks.objects.get(lesson=lesson, student=student)
                        if amount:
                            mark.amount = amount
                            mark.save()
                        else:
                            mark.delete()
                    except ObjectDoesNotExist:
                        if amount:
                            Marks.objects.create(lesson=lesson,
                                                 student=student,
                                                 amount=amount,
                                                 subject=subject,
                                                 date=lesson.date,
                                                 )
                return redirect(diary)
        else:
            return render(request, 'teacher.html', context)
    else:
        redirect('/')


@login_required(login_url="login")
@allowed_users(allowed_roles=['students'], message="Доступ к этой странице имеют только ученики.")
def stats(request, id):
    student = Students.objects.get(account=request.user)
    grade = student.grade
    try:
        subject = Subjects.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request,'error.html', context={'title':'Мы не можем найти то, что Вы ищите.',
                                                     'error':'404',
                                                     'description':'Данный предмет отстуствует.'})
    #return HttpResponse(subject.name)
    lessons = Lessons.objects.filter(grade=grade, subject=subject)
    #return HttpResponse(len(lessons))
    marks = []
    #for i in lessons:
        #try: marks.append(Marks.objects.get(student=student, lesson=i))
        #except: pass
    marks = student.marks_set.filter(subject=subject)

    # If student has no marks than send him a page with info.
    # Otherwise, student will get a page with statistics and his results.
    if marks:
        n_amount = 0
        marks_list = []
        for i in marks:
            m = i.amount
            if m == -1:
                 n_amount += 1
            else:
                marks_list.append(m)
        marks_smart_list = []
        for i in marks:
            if i.amount != -1:
                marks_smart_list.append(i)
        avg = get_averange(marks_list) # Get averange of marks
        smart_avg = get_smart_averange(marks_smart_list)
        data = []
        for i in range(5, 1, -1): data.append(marks_list.count(i))
        data.append(n_amount)
        context = {
            'lessons':lessons,
            'marks':marks,
            'subject':subject,
            'data':data,
            'avg':avg,
            'smartavg':smart_avg}
        return render(request, 'results.html', context)
    return render(request, 'no_marks.html')
    subjects = grade.subjects.all()
    context = {'subjects':subjects}
    return render(request, 'diary_student.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['students'], message="Доступ к этой странице имеют только ученики.")
def homework(request):
    if request.method == "POST":
        if "day" in request.POST:
            form = DatePickForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                student = Students.objects.get(account=request.user)
                grade = student.grade
                lessons = Lessons.objects.filter(date=date, grade=grade)
            return render(request, 'homework.html', {'form':form, 'lessons':lessons, 'date':date})
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=6)
    lessons = Lessons.objects.filter(date__range=[start_date, end_date])
    form = DatePickForm()
    return render(request, 'homework.html', {'form':form, 'lessons':lessons})


@login_required(login_url="login")
@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
def add_student_page(request):
    """
    Page where teachers can add students to their grade.
    """
    try:
        grade = Grades.objects.get(main_teacher=request.user.id)
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': "Вы не классный руководитель."})
    students = Students.objects.filter(grade=grade)

    if request.method == "POST":
        form = AddStudentToGradeForm(request.POST)
        if form.is_valid:
            fn = request.POST.get('first_name')
            s = request.POST.get('surname')
            search = Students.objects.filter(first_name=fn, surname=s)
            context = {'form': form, 'search': search, 'grade': grade, 'students': students}
            return render(request, 'grades/add_student.html', context)

    form = AddStudentToGradeForm()
    context = {'form': form, 'grade': grade, 'students': students}
    return render(request, 'grades/add_student.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
def add_student(request, i):
    """
    Function defining the process of adding new student to a grade and confirming it.
    """
    u = Users.objects.get(email=i)
    s = Students.objects.get(account=u)
    if request.method == "POST":
        try:
            grade = Grades.objects.get(main_teacher=request.user.id)
            s.grade = grade
            s.save()
            return redirect('add_student_page')
        except ObjectDoesNotExist:
            context = {'message': "Вы не классный руководитель."}
            return render(request, 'access_denied.html', context)
    else:
        return render(request, 'grades/add_student_confirm.html', {'s': s})


@login_required(login_url="login")
@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
def create_grade_page(request):
    if request.method == "POST":
        form = GradeCreationForm(request.POST)
        if form.is_valid():
            grade = form.save()
            mt = Teachers.objects.get(account=request.user)
            grade.main_teacher = mt
            grade.save()
            return redirect('my_grade')
    form = GradeCreationForm()
    context = {'form': form}
    return render(request, 'grades/add_grade.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
def my_grade(request):
    """
    Page with information about teacher's grade.
    """
    me = Teachers.objects.get(account=request.user)
    try:
        grade = Grades.objects.get(main_teacher=me)
    except ObjectDoesNotExist:
        grade = None
    context = {'grade': grade}
    return render(request, 'grades/my_grade.html', context)


def view_students_marks(request):
    me = Teachers.objects.get(account=request.user)
    try:
        grade = Grades.objects.get(main_teacher=me)
        students = Students.objects.filter(grade=grade)
        context = {
            'students':students
        }
        return render(request, 'grades/grade_marks.html', context)
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': 'Вы не являетесь классным руководителем.'})


def students_marks(request, pk):
    student = Students.objects.get(account=pk)
    me = Teachers.objects.get(account=request.user)
    try:
        grade = Grades.objects.get(main_teacher=me)
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message': 'Вы не являетесь классным руководителем.'})
        
    subjects = grade.subjects.all()
    d = {}
    max_length = 0
    for s in subjects:
        # m = Marks.objects.filter(student=student, subject=s)
        marks = student.marks_set.filter(subject=s.id)
        if len(marks) > max_length:
            max_length = len(marks)
        a, n_amount = 0, 0
        for mark in marks:
            if mark.amount != -1:
                a += mark.amount
            else:
                n_amount += 1
        if len(marks) != 0:
            d.update({s.name:[round(a/(len(marks)-n_amount),2),marks]})
        else:
            d.update({s.name:['-',[]]})

    for subject, marks in d.items():
        d.update({subject:[marks[0],marks[1],range(max_length-len(marks[1]))]})
    print(d)
    context = {
        'student': student,
        'd': d,
        'max_length':max_length

    }
    return render(request, 'view_marks.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
def delete_student(request, i):
    """
    Function defining the process of deleting a student from a grade and confirming it.
    """
    u = Users.objects.get(email=i)
    s = Students.objects.get(account=u)
    if request.method == "POST":
        try:
            grade = Grades.objects.get(main_teacher=request.user.id)
            s.grade = None
            s.save()
            return redirect('add_student_page')
        except ObjectDoesNotExist:
            context = {'message': "Вы не классный руководитель."}
            return render(request, 'access_denied.html', context)
    else:
        return render(request, 'grades/delete_student_confirm.html', {'s': s})


@allowed_users(allowed_roles=['teachers', 'students'], message="Вы не зарегистрированы как учитель или ученик.")
@login_required(login_url="login")
def admin_message(request):
    """
    Send a message to an admin.
    """
    if request.method == "POST":
        form = AdminMessageCreationForm(request.POST)
        if form.is_valid():
            m = form.save()
            m.sender = request.user
            m.save()
            return redirect('profile')
    form = AdminMessageCreationForm()
    return render(request, 'admin_messages.html', {'form': form})


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
    students = Students.objects.all()
    students = Paginator(students, 100)
    students = students.get_page(page)
    return render(request, 'students/dashboard.html', {'students': students})


@login_required(login_url="/login/")
@admin_only
def students_delete(request, id):
    """
    Delete a student.
    """
    u = Users.objects.get(email=id)
    s = Students.objects.get(account=u)
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
    u = Users.objects.get(email=id)
    s = Students.objects.get(account=u)
    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('students_dashboard')
    form = StudentEditForm(instance=s)
    return render(request, 'students/update.html', {'form': form})


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
    u = Administrators.objects.all()
    u = Paginator(u, 100)
    u = u.get_page(page)
    return render(request, 'admins/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def admins_delete(request, id):
    """
    Delete an admin.
    """
    u = Users.objects.get(email=id)
    s = Administrators.objects.get(account=u)
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
    u = Users.objects.get(email=id)
    s = Administrators.objects.get(account=u)
    if request.method == "POST":
        form = AdminsEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('admins_dashboard')
    form = AdminsEditForm(instance=s)
    return render(request, 'admins/update.html', {'form': form})


# TEACHERS SECTION

@login_required(login_url="/login/")
@admin_only
def teachers_dashboard_first_page(request):
    return redirect('/teachers/dashboard/1')


@login_required(login_url="/login/")
@admin_only
def teachers_dashboard(request, page):
    u = Teachers.objects.all()
    u = Paginator(u, 50)
    u = u.get_page(page)
    return render(request, 'teachers/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def teachers_delete(request, id):
    """
    Delete a teacher.
    """
    u = Users.objects.get(email=id)
    s = Teachers.objects.get(account=u)
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
    u = Users.objects.get(email=id)
    s = Teachers.objects.get(account=u)
    if request.method == "POST":
        form = TeacherEditForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('teachers_dashboard')
    form = TeacherEditForm(instance=s)
    return render(request, 'teachers/update.html', {'form': form})


def homepage(request):
    """
    Return a homepage.
    """
    return render(request, 'homepage.html')


def social(request):
    """
    Return a page with link to gymnasium's social pages.
    """
    return render(request, 'social.html')


def get_help(request):
    """
    Return a page with help information.
    """
    return render(request, 'docs.html')


def error404(request):
    return render(request, 'error.html', {
        'error': "404",
        'title': "Страница не найдена.",
        "description": "Мы не можем найти страницу, которую вы ищите."
    })


def error500(request):
    return render(request, 'error.html', {
        'error': "500",
        'title': "Что-то пошло не так",
        "description": "Мы работаем над этим."
    })
