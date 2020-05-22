"""
This function don't return render
"""

import datetime
from . import models
from . import forms

TERMS = (
    ((1, 7), (27, 10)),
    ((3, 11), (29, 12)),
    ((12, 1), (21, 3)),  # FIX ON PRODUCTION
    ((29, 3), (27, 5))
)


def get_average(marks_list):
    """
    Calculate the average for Marks QuerySet.
    Return a tuple of average, marks' sum and total marks amount.
    """
    if len(marks_list) == 0:
        return '-'
    grades = sum([i.amount for i in marks_list])
    return round(grades / len(marks_list), 2), grades, len(marks_list)


def get_smart_average(list) -> float:
    if len(list) == 0:
        return "-"
    s = 0
    w = 0
    for i in list:
        weight = i.lesson.control.weight
        s += weight * i.amount
        w += weight
    return round(s / w, 2)


def increase_avg(mark, avg):
    """
    Adds mark to average list ignoring year & quarter
    marks and lesson missing marks.
    """
    if mark.amount != -1 and mark.lesson.control.weight != 100:
        avg[mark.student_id][0] += mark.amount * mark.lesson.control.weight
        avg[mark.student_id][1] += mark.lesson.control.weight
        avg[mark.student_id][2] += mark.amount
        avg[mark.student_id][3] += 1


def create_table(grade, subject, quarter):
    lessons = {
        lesson.id: lesson for lesson in
        models.Lessons.objects.filter(
            grade=grade, subject=subject, quarter=quarter).select_related("control").order_by(
            "date").all()
    }
    students = {
        student.account_id: student for student in
        models.Students.objects.filter(
            grade=grade).order_by("surname", "first_name", "second_name")
    }

    marks = models.Marks.objects.filter(
        student__grade_id=grade.id,
        lesson__grade_id=grade.id,
        lesson__subject_id=subject.id,
        lesson__quarter=quarter,
    )

    scope = {}
    avg = {}
    for mark in marks:
        if students[mark.student_id] not in scope:
            scope[students[mark.student_id]] = {}
        lesson = lessons[mark.lesson_id]
        scope[students[mark.student_id]].update({lesson: mark})
        if mark.student_id in avg:
            increase_avg(mark, avg)
        else:
            avg[mark.student_id] = [0, 0, 0, 0]
            increase_avg(mark, avg)

    for sk, student in students.items():
        for lk, lesson in lessons.items():
            if student not in scope:
                scope[student] = {}
                avg[student.pk] = [0, 0, 0, 0]
            if lesson not in scope[student]:
                scope[student].update({lesson: None})

    scope = sorted(list(scope.items()), key=lambda student: student[0].surname)

    return {
        'is_post': True,
        'lessons': lessons,
        'scope': scope,
        'avg': avg
    }


def create_controls(grade, subject, term):
    controls = models.Controls.objects.all()
    controls = term_valid(controls)
    controls = year_valid(controls)
    lessons = models.Lessons.objects.filter(grade=grade, subject=subject, quarter=term).all()
    for lesson in lessons:
        if lesson.control.name == 'Четвертная оценка':
            controls = controls.exclude(name='Четвертная оценка')
        if lesson.control.name == 'Годовая оценка':
            controls = controls.exclude(name='Годовая оценка')
    return controls


def check_if_teacher_has_class(teacher):
    """
    Check if teacher has a class. If does, return
    Grades object. Otherwise, return False.
    """
    if teacher.grades_set.all():
        return teacher.grades_set.all()[0]
    return False


def get_current_quarter() -> int:
    """
    Return current quarter, 0 if now is holidays' time.
    """
    today = datetime.date.today()
    for q in models.Quarters.objects.all():
        if q.begin <= today <= q.end:
            return q.number
    return 0


def term_valid(controls):
    """
    Check if teacher can create lesson with quarter mark control.
    """
    for q in models.Quarters.objects.all():
        delta = q.end - datetime.date.today()
        if delta.days < 14:
            return controls
    return controls.exclude(name='Четвертная оценка')


def get_quarter_by_date(datestring: str) -> int:
    """
    Return a number of quarter by a date stamp string.
    If quarter does not exist, return 0 instead.
    """
    converted_date = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    for q in models.Quarters.objects.all():
        if q.begin <= converted_date <= q.end:
            return q.number
    return 0


def year_valid(controls):
    """
    Check if teacher can create lesson with year mark control.
    """
    fourth = models.Quarters.objects.get(number=4)
    delta = fourth.end - datetime.date.today()
    if delta.days < 14:
        return controls
    return controls.exclude(name='Годовая оценка')


def each_contains(d: dict, elements) -> bool:
    """
    Check if each element from list is in dictionary.
    """
    for el in elements:
        if el not in d:
            return False
    return True


def update_context(context, class_, term, subject):
    context.update(create_table(
        grade=class_,
        subject=subject,
        quarter=term))
    context.update({'contols': create_controls(
        grade=class_,
        subject=subject,
        term=term)})


def check_if_student_in_class(student: models.Students) -> bool:
    return student.grade is not None


def get_session_data_diary(session, classes, subjects):
    grade = classes.get(id=session['grade'])
    subject = subjects.get(id=session['subject'])
    term = session['term']
    return grade, subject, term


def get_session_data(session):
    grade = models.Grades.objects.get(id=session['grade'])
    subject = models.Subjects.objects.get(id=session['subject'])
    term = session['term']
    return grade, subject, term


def create_lesson_form(context):
    context.update({'form': forms.LessonCreationForm()})


def load_to_session(session, **kwargs):
    for i in kwargs:
        session[i] = kwargs[i]


def fool_teacher_protection(teacher, lesson: models.Lessons):
    """
    Returns False if teacher doesn't have an access to the lesson.
    """
    teacher = models.Teachers.objects.get(pk=teacher)
    classes = models.Grades.objects.filter(main_teacher=teacher)
    subjects = teacher.subjects.all()
    if lesson.grade not in classes or lesson.subject not in subjects:
        return False
    return True
