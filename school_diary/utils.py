from apps.core import models


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
    available_grades = models.Klasses.objects.filter(
        teachers=teacher).order_by('number', 'letter')
    return available_subjects, available_grades


def get_group(subject, klass) -> models.Groups:
    """
    Return group from given subject and class.
    If group hasn't been created yet, set
    default students for new group and return it.
    """
    group, created = models.Groups.objects.get_or_create(
        klass=klass,
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
        current_quarter = models.Quarters.get_default_quarter()
        group = get_group(subjects[0], grades[0])
        load_into_session(session, {
            'group': group.id,
            'term': current_quarter.id,
        })


def fool_teacher_protection(teacher: models.Teachers, lesson: models.Lessons):
    """
    Return False if teacher doesn't have an access to the lesson.
    """
    subjects, grades = grades_and_subjects(teacher)
    if lesson.group.grade not in grades or lesson.group.subject not in subjects:
        return False
    return True
