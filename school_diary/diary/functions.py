import datetime
from typing import List
from functools import reduce
from django.db.models import Q
from . import models


def get_marks_data(marks):
    """
    Take Marks QuerySet and get a smart average, average,
    marks quantity, list of all marks' amounts, needed
    mark and a number of lesson have been missed.
    """
    data = [0, 0, 0, 0, [], 0]
    # data[0] - sum of products of marks' amounts and weights
    # data[1] - sum of marks' weights
    # data[2] - sum of marks' amounts
    # data[3] - marks' quantity
    # data[4] - list of marks' amounts
    # data[5] - how many lesson have been missed
    for mark in marks:
        if mark.amount == -1:
            data[5] += 1
            continue
        if mark.lesson.control.weight != 100:
            data[0] += mark.amount * mark.lesson.control.weight
            data[1] += mark.lesson.control.weight
            data[2] += mark.amount
            data[3] += 1
            data[4].append(mark.amount)
    avg = data[2] / data[3]  # Average
    return (
        round(data[0] / data[1], 2),  # Smart average
        round(avg, 2),  # Average
        data[3],  # Marks quantity
        data[4],  # List of amounts of all marks
        get_needed_mark(data[2:4], avg),
        data[5]
    )


def get_needed_mark(data, avg):
    """
    Give a number of '5's needed to get
    a certain mark in quarter result. Return 2
    values: an amount and what mark is needed to get.
    """
    needed, needed_mark = 0, 0
    if avg <= 4.5:
        needed = 9 * data[1] - 2 * data[0] + 1
        needed_mark = 5
    if avg <= 3.5:
        needed = (7 * data[1] - 2 * data[0]) // 3 + 1
        needed_mark = 4
    if avg <= 2.5:
        needed = (5 * data[1] - 2 * data[0]) // 5 + 1
        needed_mark = 3
    return needed, needed_mark


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
        if mark.student_id not in avg:
            avg[mark.student_id] = [0, 0, 0, 0]
        if mark.amount != -1 and mark.lesson.control.weight != 100:
            avg[mark.student_id][0] += mark.amount * mark.lesson.control.weight
            avg[mark.student_id][1] += mark.lesson.control.weight
            avg[mark.student_id][2] += mark.amount
            avg[mark.student_id][3] += 1

    for sk, student in students.items():
        for lk, lesson in lessons.items():
            if student not in scope:
                scope[student] = {}
                avg[student.pk] = [0, 0, 0, 0]
            if lesson not in scope[student]:
                scope[student].update({lesson: None})
    # Sort the scope by students' surnames
    scope = sorted(list(scope.items()), key=lambda student: student[0].surname)
    return {
        'is_post': True, 'lessons': lessons,
        'scope': scope, 'avg': avg
    }


def create_controls(grade, subject, term):
    """
    Filter controls a teacher can use.
    """
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
    """
    Show if student is in grade or not.
    """
    return student.grade is not None


def get_session_data(session, grades=None, subjects=None):
    """
    Get current grade, subject and term stored in session.
    """
    grade = grades.get(id=session['grade']) if grades else \
        models.Grades.objects.get(id=session['grade'])
    subject = subjects.get(id=session['subject']) if subjects else \
        models.Subjects.objects.get(id=session['subject'])
    term = session['term']
    return grade, subject, term


def load_to_session(session, **kwargs):
    """
    Take some kwargs and load them into current session.
    """
    for i in kwargs:
        session[i] = kwargs[i]


def fool_teacher_protection(teacher, lesson: models.Lessons):
    """
    Return False if teacher doesn't have an access to the lesson.
    """
    teacher = models.Teachers.objects.get(pk=teacher)
    grades = models.Grades.objects.filter(main_teacher=teacher)
    subjects = teacher.subjects.all()
    if lesson.grade not in grades or lesson.subject not in subjects:
        return False
    return True


def save_marks(post_data, grade, subject) -> None:
    """
    Save marks to database from POST data.
    """
    marks_dict = {
        tuple(map(int, k.replace("mark_", "").split("|"))): str(post_data[k])
        for k in dict(post_data)
        if k.startswith('mark_')
    }
    marks_raw = models.Marks.objects.select_for_update().filter(
        student__grade_id=grade.id,
        lesson__grade_id=grade.id,
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


def add_comment_to_mark(post_data):
    """
    Add a comment to marks using provided POST data.
    """
    comment = post_data.get('comment')
    data = post_data.get('commentdata')
    student_id, lesson_id = data.split("|")[1]
    student = models.Students.objects.get(account=student_id)
    lesson = models.Lessons.objects.get(id=lesson_id)
    mark = models.Marks.objects.get(student=student, lesson=lesson)
    mark.comment = comment
    mark.save()


class Homework(object):
    """
    A class representing one homework for specified date & subject.

    Attributes:
        date:
            A datetime.date instance indicating homework date.
        subject:
            A diary.models.Subjects instance indicating homework subject.
        text:
            A string with task description.
        file:
            A string with link to a file that was attached to the task description.
        file_exists:
            A boolean that shows if file is attached to the task.
    """
    def __init__(self, lesson: models.Lessons):
        self.date = lesson.date
        self.subject = lesson.subject
        self.text = lesson.homework
        self.file = lesson.h_file

    @property
    def file_exists(self):
        """Show if homework task has an attached file."""
        return bool(self.file)


def get_homework(
        grade: models.Lessons,
        start_date: datetime.date,
        end_date: datetime.date = None) -> List[Homework]:
    """
    Get homework for specified grade. If both start_date and end_date are
    specified, search for homework in this time range. Otherwise (only start_date)
    search for homework only for start_date.

    Args:
        grade:
            diary.models.Grades instance that means a grade where search is performed.
        start_date:
            A datetime.date instance, date for which a search is performed.
        end_date:
            Optional; A datetime.date instance. If it's provided, start_date turns
            into a start date of time range and end_date will mean an end of this range.

    Returns:
        A list of diary.functions.Homework objects.
    """
    if end_date is not None:
        queryset = models.Lessons.objects.filter(
            Q(homework__iregex=r'\S+') | Q(h_file__iregex=r'\S+'),
            grade=grade,
            date__range=(start_date, end_date))
    else:
        queryset = models.Lessons.objects.filter(
            Q(homework__iregex=r'\S+') | Q(h_file__iregex=r'\S+'),
            grade=grade, date=start_date)
    return [Homework(i) for i in queryset]
