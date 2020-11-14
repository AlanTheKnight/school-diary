import datetime
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
    avg, sm_avg = calculate_avg(data)
    return (
        sm_avg,
        avg,
        data[3],  # Marks quantity
        data[4],  # List of amounts of all marks
        (get_needed_mark(data[2:4], avg) if avg != '-' else '-'),
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


def create_table(group, quarter):
    # Dictionary of all lessons that are connected to group & quarter
    # if control which they are relating to is not None and
    # order them by date.
    lessons = {
        lesson.id: lesson for lesson in
        models.Lessons.objects.filter(
            group=group, quarter=quarter).select_related("control").order_by(
            "date").all()
    }
    # Select all students which are related to group.
    students = {
        student.account_id: student for student in
        group.students.filter(grade=group.grade)
    }

    # Select all marks which are related to group & quarter.
    marks = models.Marks.objects.filter(
        lesson__group_id=group.id,
        lesson__quarter=quarter,
        student__in=students,
    )

    # Scope:
    # {
    #   student1: {
    #       "avg": avg, "sm_avg": sm_avg,
    #       lesson1: mark, lesson2: mark, ...},
    #   student2: {
    #       "avg": avg, "sm_avg": sm_avg,
    #       lesson1: mark, lesson2: mark, ...},
    # }

    scope = {}
    avg = {}
    for mark in marks:
        if mark.student not in scope:
            scope[mark.student] = {}
        scope[mark.student][mark.lesson] = mark
        if mark.student not in avg:
            avg[mark.student] = [0, 0, 0, 0]
        # Change average & smart average and bypass missing lessons
        # or year/quarter marks.
        if mark.amount != -1 and mark.lesson.control.weight != 100:
            avg[mark.student][0] += mark.amount * mark.lesson.control.weight
            avg[mark.student][1] += mark.lesson.control.weight
            avg[mark.student][2] += mark.amount
            avg[mark.student][3] += 1

    for sk, student in students.items():
        for lk, lesson in lessons.items():
            if student not in scope:
                scope[student] = {}
                avg[student] = [0, 0, 0, 0]
            if lesson not in scope[student]:
                scope[student][lesson] = None

    for student in scope:
        scope[student]["avg"] = calculate_avg(avg[student])
    # Sort the scope by students' surnames
    scope = sorted(list(scope.items()), key=lambda student: student[0].surname)
    return {'lessons': lessons, 'scope': scope}


def calculate_avg(data: list):
    avg = round(data[2] / data[3], 1) if data[3] != 0 else '-'
    sm_avg = round(data[0] / data[1], 1) if data[1] != 0 else '-'
    return (avg, sm_avg)


def create_controls(group, term):
    """
    Filter controls a teacher can use.
    """
    controls = models.Controls.objects.all()
    controls = term_valid(controls)
    controls = year_valid(controls)
    lessons = models.Lessons.objects.filter(group=group, quarter=term).all()
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


def update_context(context, group, term):
    context.update(create_table(
        group=group,
        quarter=term))
    context.update({'contols': create_controls(
        group=group,
        term=term)})


def check_if_student_in_class(student: models.Students) -> bool:
    """
    Show if student is in grade or not.
    """
    return student.grade is not None


def load_to_session(session, **kwargs):
    """
    Take some kwargs and load them into current session.
    """
    for i in kwargs:
        session[i] = kwargs[i]


def session_is_ok(session):
    """Show if session contains values needed to render teacher.html"""
    return (
        'grade' in session and
        'subject' in session and
        'term' in session
    )
