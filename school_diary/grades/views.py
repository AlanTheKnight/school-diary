import datetime
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import diary.models as models
from . import forms
from diary.decorators import teacher_only
import diary.functions as functions


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
