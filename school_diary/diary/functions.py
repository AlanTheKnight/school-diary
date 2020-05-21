"""
This function don't return render
"""

import datetime
from . import models

TERMS = (
    ((1, 7), (27, 10)),
    ((3, 11), (29, 12)),
    ((12, 1), (21, 3)),  # FIX ON PRODUCTION
    ((29, 3), (27, 5))
)


def get_average(list):
    if len(list) == 0:
        return '-'
    grades = sum([i.amount for i in list])
    return round(grades / len(list), 2), grades, len(list)


def get_smart_average(list):
    if len(list) == 0:
        return "-"
    s = 0
    w = 0
    for i in list:
        weight = i.lesson.control.weight
        s += weight * i.amount
        w += weight
    return round(s / w, 2)


def create_table(grade, subject, quarter):
    lessons = {
        lesson.id: lesson for lesson in
        models.Lessons.objects.filter(grade=grade, subject=subject, quarter=quarter).select_related("control").order_by(
            "date").all()
    }
    students = {student.account_id: student for student in
                models.Students.objects.filter(grade=grade).order_by("surname", "first_name", "second_name")}

    marks = models.Marks.objects.filter(
        student__grade_id=grade.id,
        lesson__grade_id=grade.id,
        lesson__subject_id=subject.id,
        lesson__quarter=quarter,
    )

    scope = {}
    avg = {}
    for mark in marks:
        def increase_avg(mark):
            if mark.amount != -1 and mark.lesson.control.weight != 100:
                avg[mark.student_id][0] += mark.amount * mark.lesson.control.weight
                avg[mark.student_id][1] += mark.lesson.control.weight
                avg[mark.student_id][2] += mark.amount
                avg[mark.student_id][3] += 1
        if students[mark.student_id] not in scope:
            scope[students[mark.student_id]] = {}
        lesson = lessons[mark.lesson_id]
        scope[students[mark.student_id]].update({lesson: mark})
        if mark.student_id in avg:
            increase_avg(mark)
        else:
            avg[mark.student_id] = [0, 0, 0, 0]
            increase_avg(mark)

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
        'subject_id': subject.id,
        'grade_id': grade.id,
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
    return {'controls': controls}


def check_if_teacher_has_class(teacher):
    if teacher.grades_set.all():
        return True
    return False


def get_current_quarter() -> int:
    """
    Return current quarter, 0 if now is holidays' time.
    """
    today = datetime.date.today()
    for quarter in models.Quarters.objects.all():
        if quarter.start <= today <= quarter.end:
            return quarter
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
        if q.start <= converted_date <= q.end:
            return q.number
    return 0


def year_valid(controls):
    """
    Check if teacher can create lesson with year mark control.
    """
    fourth = models.Quarters.get(number=4)
    delta = fourth - datetime.date.today()
    if delta.days < 14:
        return controls
    return controls.exclude(name='Годовая оценка')
