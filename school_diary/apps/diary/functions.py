import datetime
from apps.core import models


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
