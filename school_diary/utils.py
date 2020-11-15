import datetime
from typing import Union
from diary import models


def get_current_quarter() -> int:
    """
    Return current quarter, 0 if now is holidays' time.
    """
    today = datetime.date.today()
    for q in models.Quarters.objects.all():
        if q.begin <= today <= q.end:
            return q.number
    return 0


def get_quarter_by_date(date: Union[str, datetime.date]) -> int:
    """
    Return a number of quarter by a date
    stamp string or date object.
    If quarter does not exist, return 0 instead.

    Args:
        date: datestring or datetime.date instance
    """
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    for q in models.Quarters.objects.all():
        if q.begin <= date <= q.end:
            return q.number
    return 0


def load_from_session(session, values: dict) -> dict:
    """
    Loads data from session.

    Args:
        session: current session.
        values: dict containing needed values and their
            default values.
    """
    out = {}
    for key in values:
        out[key] = session.get(key, values[key])
    return out


def load_into_session(session, values: dict) -> None:
    """
    Loads data into the session.

    Args:
        session: current session
        values: dict containing values to load into session.
    """
    for key in values:
        session[key] = values[key]


def get_default_quarter():
    def_term = get_current_quarter()
    if def_term == 0:
        def_term = 1
    return def_term


def each_contains(d: dict, values: list):
    for i in values:
        if i not in d:
            return False
    return True


def grades_and_subjects(teacher: models.Teachers) -> tuple:
    """
    Return all subjects & grades where user is a
    teacher.
    """
    available_subjects = teacher.subjects.all().order_by('name')
    available_grades = models.Grades.objects.filter(
        teachers=teacher).order_by('number', 'letter')
    return available_subjects, available_grades


def get_group(subject, grade) -> models.Groups:
    """
    Return group from given subject and class.
    If group hasn't been created yet, set
    default students for new group and return it.
    """
    group, created = models.Groups.objects.get_or_create(
        grade=grade,
        subject=subject
    )
    if created:
        group.set_default_students()
    return group


def session_ok(session) -> bool:
    return each_contains(session, ("term", "group"))


def set_default_session(session, subjects, grades) -> None:
    if not grades:
        raise ValueError("Grades length needs to be > 0.")
    if not subjects:
        raise ValueError("Subjects length needs to be > 0.")
    if not each_contains(session, ("term", "group")):
        current_quarter = get_current_quarter()
        if not current_quarter:
            current_quarter = 1
        group = get_group(subjects[0], grades[0])
        load_into_session(session, {
            'group': group.id,
            'term': current_quarter,
        })


def fool_teacher_protection(teacher: models.Teachers, lesson: models.Lessons):
    """
    Return False if teacher doesn't have an access to the lesson.
    """
    subjects, grades = grades_and_subjects(teacher)
    if lesson.group.grade not in grades or lesson.group.subject not in subjects:
        return False
    return True
