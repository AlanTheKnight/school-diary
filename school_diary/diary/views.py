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


@unauthenticated_user
def user_register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Учётная запись была создана успешно.")
            return redirect('/diary/login')
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
        print(user)
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
    return redirect('/diary/login/')


@login_required(login_url="/diary/login/")
def user_profile(request):
    if request.user.account_type == 0:
        data = Users.objects.get(email=request.user)
    if request.user.account_type == 1:
        data = Administrators.objects.get(account=request.user)
    if request.user.account_type == 2:
        data = Teachers.objects.get(account=request.user)
    if request.user.account_type == 3:
        data = Students.objects.get(account=request.user)
    context = {'data':data}
    return render(request, 'profile.html', context)


@login_required(login_url="/diary/login/")
@admin_only
def admin_register(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый администратор был создан успешно.")
            return redirect('/diary/login/')
    if request.POST:
        form = AdminSignUpForm(request.POST)
    else:
        form = AdminSignUpForm()
    return render(request, 'registration_admin.html', {'form': form, 'error': 0})


@login_required(login_url="/diary/login/")
@admin_only
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый учитель был создан успешно.")
            return redirect('/diary/login/')
    if request.POST:
        form = TeacherSignUpForm(request.POST)
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration_teacher.html', {'form': form, 'error': 0})


def create_table(lessons, students):
    scope = {}
    for student in students:
        stu = {}
        for lesson in lessons:
            try:
                stu.update({lesson: student.marks_set.get(lesson=lesson)})
            except ObjectDoesNotExist:
                stu.update({lesson: None})
        scope.update({student: stu})
    return scope


@login_required(login_url="/diary/login/")
def create_lesson(request):
    form = LessonCreationForm()
    context = {'form': form}
    return render(request, 'create_lesson.html', context)


@login_required(login_url="/diary/login/")
def diary(request):
    if request.user.account_type == 0 or request.user.account_type == 1:
        return render(request, 'diary_admin_main.html')

    elif request.user.account_type == 3:
        messages.error(request, 'Пока не готово')
        return redirect('/')
        
        student = Students.objects.get(account=request.user)
        context = {'Student': student,
                   'subjects': Subjects.objects.all(),
                   'daylist': ['09.02', '10.02', '11.02'],
                   'marks': student.mark_set.order_by('date')}
        return render(request, 'student.html', context)

    elif request.user.account_type == 2:
        teacher = Teachers.objects.get(account=request.user)
        context = {'Teacher': teacher,
                   'subjects': teacher.subjects.all(),
                   'grades': Grades.objects.filter(teachers=teacher),
                   'is_post': False
                   }

        if request.method == 'POST':
            if request.POST.get('subject'):
                subject = Subjects.objects.get(name=request.POST.get('subject'))
                number = int(request.POST.get('grade')[0])
                letter = request.POST.get('grade')[1]
                try:
                    grade = Grades.objects.get(number=number, subjects=subject, letter=letter, teachers=teacher)
                except ObjectDoesNotExist:
                    messages.error(request, 'Ошибка')
                    return render(request, 'teacher.html', context)

                lessons = Lessons.objects.filter(grade=grade, subject=subject)
                students = Students.objects.filter(grade=grade)
                scope = create_table(lessons, students)
                print(scope)
                context.update({
                    'is_post': True,
                    'lessons': lessons,
                    'scope': scope
                })
                return render(request, 'teacher.html', context)
            else:
                for i in dict(request.POST):
                    if i == 'csrfmiddlewaretoken':
                        continue
                    print(i.split('|'))
                    li = i.split('|')
                    account = li[0]
                    id_les = li[1]
                    print(account, id_les)
                    student = Students.objects.get(account=Users.objects.get(email=account))
                    lesson = Lessons.objects.get(pk=id_les)
                    amount = str(request.POST[i])
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
                                                 amount=amount)
                        else:
                            pass
                return render(request, 'teacher.html', context)
        else:
            return render(request, 'teacher.html', context)
    else:
        redirect('/')


@login_required(login_url="login")
@allowed_users(allowed_roles=['teachers'], message="Вы не зарегистрированы как учитель.")
def add_student_page(request):
    """
    Page where teachers can add students to their grade.
    """
    try:
        grade = Grades.objects.get(main_teacher=request.user.id)
    except ObjectDoesNotExist:
        return render(request, 'access_denied.html', {'message':"Вы не классный руководитель."})
    students = Students.objects.filter(grade=grade)

    if request.method == "POST":
        form = AddStudentToGradeForm(request.POST)
        if form.is_valid:
            fn = request.POST.get('first_name')
            s = request.POST.get('surname')
            search = Students.objects.filter(first_name=fn, surname=s)
            context = {'form':form, 'search':search, 'grade':grade, 'students':students}
            return render(request, 'grades/add_student.html', context)
    
    form = AddStudentToGradeForm()
    context = {'form':form, 'grade':grade, 'students':students}
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
            context = {'message':"Вы не классный руководитель."}
            return render(request, 'access_denied.html', context)
    else:
        return render(request, 'grades/add_student_confirm.html', {'s':s})


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
    context = {'form':form}
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
    context = {'grade':grade}
    return render(request, 'grades/my_grade.html', context)


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
            context = {'message':"Вы не классный руководитель."}
            return render(request, 'access_denied.html', context)
    else:
        return render(request, 'grades/delete_student_confirm.html', {'s':s})


@allowed_users(allowed_roles=['teachers', 'students'], message="Вы не зарегистрированы как учитель или ученик.")
@login_required(login_url="login")
def admin_message(request):
    if request.method == "POST":
        form = AdminMessageCreationForm(request.POST)
        if form.is_valid():
            m = form.save()
            m.sender = request.user
            m.save()
            return redirect('profile')
    form = AdminMessageCreationForm()
    return render(request, 'admin_messages.html', {'form':form})


@login_required(login_url="/diary/login/")
@admin_only
def students_dashboard_first_page(request):
    return redirect('/diary/students/dashboard/1')


@login_required(login_url="/diary/login/")
@admin_only
def students_dashboard(request, page):
    students = Students.objects.all()
    students = Paginator(students, 100)
    students = students.get_page(page)
    return render(request, 'students/dashboard.html', {'students':students})


@login_required(login_url="/diary/login/")
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
    return render(request, 'students/delete.html', {'s':s})


@login_required(login_url="/diary/login/")
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
    return render(request, 'students/update.html', {'form':form})


@login_required(login_url="/diary/login/")
@admin_only
def admins_dashboard_first_page(request):
    """
    Redirect user to the first page of admin dashboard.
    """
    return redirect('/diary/admins/dashboard/1')


@login_required(login_url="/diary/login/")
@admin_only
def admins_dashboard(request, page):
    """
    Send dashboard with up to 100 administrators
    """
    u = Administrators.objects.all()
    u = Paginator(u, 100)
    u = u.get_page(page)
    return render(request, 'admins/dashboard.html', {'users':u})


@login_required(login_url="/diary/login/")
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
    return render(request, 'admins/delete.html', {'s':s})


@login_required(login_url="/diary/login/")
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
    return render(request, 'admins/update.html', {'form':form})


# TEACHERS SECTION

@login_required(login_url="/diary/login/")
@admin_only
def teachers_dashboard_first_page(request):
    return redirect('/diary/teachers/dashboard/1')


@login_required(login_url="/diary/login/")
@admin_only
def teachers_dashboard(request, page):
    u = Teachers.objects.all()
    u = Paginator(u, 50)
    u = u.get_page(page)
    return render(request, 'teachers/dashboard.html', {'users':u})


@login_required(login_url="/diary/login/")
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
    return render(request, 'teachers/delete.html', {'s':s})


@login_required(login_url="/diary/login/")
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
    return render(request, 'teachers/update.html', {'form':form})