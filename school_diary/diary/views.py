import datetime
from functools import reduce
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import forms
from .decorators import teacher_only, student_only
from . import models
from . import functions


# Tuple of keys needed to be in request.session
# whan a teachers works with diary.
NEEDED_IN_SESSION = ('grade', 'subject', 'term')


@teacher_only
@login_required(login_url="/login/")
@transaction.atomic
def lesson_page(request, pk):
    """Page where teachers can edit lesson."""

    # If teacher haven't chosen grade, term and subject, redirect back to diary.
    if not functions.each_contains(request.session, NEEDED_IN_SESSION):
        return redirect('diary')
    lesson = models.Lessons.objects.get(pk=pk)
    form = forms.LessonCreationForm(instance=lesson)
    grade, subject, term = functions.get_session_data(request.session)
    form.fields["control"].queryset = functions.create_controls(grade, subject, term)

    if request.method == "POST":
        form = forms.LessonCreationForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            deletefile = request.POST.get("deletefile") is not None
            form.save(subject=subject, grade=grade, deletefile=deletefile)
            return redirect('diary')
    context = {'form': form, 'lesson': lesson}
    return render(request, 'lesson_page.html', context)


@login_required(login_url='/login/')
@teacher_only
def delete_lesson(request, pk):
    """
    Asks teacher's confirmation and then deletes the selected lesson.
    """
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
            avg = functions.get_average(marks_list)
            smart_avg = functions.get_smart_average(marks_list)
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
    teacher = models.Teachers.objects.get(account=request.user)  # Current teacher
    available_classes = models.Grades.objects.filter(teachers=teacher).order_by('number', 'letter')
    available_subjects = teacher.subjects.all().order_by('name')

    if not (available_classes and available_subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    if request.method == 'POST' and 'getgrade' in request.POST:
        # Teacher has just chosen class, term and subject.
        # This part of code saves chosen data to session and builds up
        # a table with marks.
        subject = available_subjects.get(name=request.POST.get('subject'))
        grade = request.POST.get('grade')
        term = int(request.POST.get('term'))
        grade = available_classes.get(number=int(grade[0:-1]), subjects=subject, letter=grade[-1])
        functions.load_to_session(
            request.session,
            term=term, subject=subject.id, grade=grade.id
        )
        return redirect('diary')

    if not functions.each_contains(request.session, NEEDED_IN_SESSION):
        current_quarter = functions.get_current_quarter()
        if not current_quarter:
            current_quarter = 1
        request.session['subject'] = available_subjects[0].id  # Loading default data into session
        request.session['grade'] = available_classes[0].id
        request.session['term'] = current_quarter

    # Creating table with marks and setting up available controls.
    grade_, subject_, term_ = functions.get_session_data_diary(
        request.session, available_classes, available_subjects)

    form = forms.LessonCreationForm()

    context = {
        'TEACHER': teacher,
        'subjects': available_subjects,
        'grades': available_classes,
        'current_class': grade_,
        'current_term': term_,
        'current_subject': subject_,
        'form': form
    }

    if request.method == "POST":

        if 'createlesson' in request.POST:
            # Teacher creates a new lesson.
            form = forms.LessonCreationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(subject=subject_, grade=grade_)

        elif 'addcomment' in request.POST:
            comment = request.POST.get('comment')
            data = request.POST.get('commentdata')
            student_id = data.split("|")[0]
            lesson_id = data.split("|")[1]
            student = models.Students.objects.get(account=student_id)
            lesson = models.Lessons.objects.get(id=lesson_id)
            mark = models.Marks.objects.get(student=student, lesson=lesson)
            mark.comment = comment
            mark.save()

        else:
            # Save marks block
            marks_dict = {
                tuple(map(int, k.replace("mark_", "").split("|"))): str(request.POST[k])
                for k in dict(request.POST)
                if k.startswith('mark_')
            }
            marks_raw = models.Marks.objects.select_for_update().filter(
                student__grade_id=grade_.id,
                lesson__grade_id=grade_.id,
                lesson__subject_id=subject_.id
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
                models.Marks(lesson_id=k[1], student_id=k[0], amount=int(v), subject=subject_)
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

    functions.update_context(context, grade_, term_, subject_)
    return render(request, 'teacher.html', context)


@login_required(login_url="/login/")
def diary(request):
    """
    Main function for displaying diary pages to admins/teachers/students.
    """
    # If user is admin
    if request.user.account_type == 0 or request.user.account_type == 1:
        return redirect('admin_panel')
    # If user is student
    elif request.user.account_type == 3:
        return students_diary(request)
    # If user is teacher
    elif request.user.account_type == 2:
        return teachers_diary(request)
    else:
        redirect('homepage')


@login_required(login_url="login")
@student_only
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

        avg = functions.get_average(marks_list)
        smart_avg = functions.get_smart_average(marks_list)

        marks_amounts = [
            i.amount for i in marks if i.amount != -1 and i.lesson.control.weight != 100
        ]
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
                context = {'form': form, 'lessons': lessons, 'date': date}
                return render(request, 'homework.html', context)
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=6)
    lessons = models.Lessons.objects.filter(
        date__range=[start_date, end_date], grade=grade, homework__iregex=r'\S+')
    if not lessons:
        lessons = models.Lessons.objects.filter(
            date__range=[start_date, end_date], grade=grade, h_file__iregex=r'\S+')
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
        term = functions.get_quarter_by_date(str(datetime.date.today()))

    class_ = functions.check_if_teacher_has_class(me)
    if class_:
        students = models.Students.objects.filter(grade=class_)
        context = {
            'students': students,
            'term': term,
        }
        return render(request, 'grades/grade_marks.html', context)
    else:
        return render(request, 'access_denied.html', {
                'message': 'Вы не являетесь классным руководителем.'
            })


def students_marks(request, pk, term):
    student = models.Students.objects.get(account=pk)
    me = models.Teachers.objects.get(account=request.user)
    my_class = functions.check_if_teacher_has_class(me)
    if not my_class:
        return render(request, 'access_denied.html', {
                'message': 'Вы не являетесь классным руководителем.'
            })
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

        avg = functions.get_average(marks_list)
        smart_avg = functions.get_smart_average(marks_list)
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


@login_required(login_url="login")
@teacher_only
def mygradesettings(request):
    me = models.Teachers.objects.get(account=request.user)
    class_ = functions.check_if_teacher_has_class(me)
    if class_:
        if request.method == "POST":
            form = forms.ClassSettingsForm(request.POST, instance=class_)
            if form.is_valid():
                form.save()
                return redirect('my_grade')
        form = forms.ClassSettingsForm(instance=class_)
        return render(request, 'grades/class_settings.html', {'form': form})
    return render(request, 'access_denied.html', {'message': 'Вы не классный руководитель.'})
