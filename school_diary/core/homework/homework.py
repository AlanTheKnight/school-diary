from core import models
from typing import Union
from django.db.models import Q
import datetime
import utils


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
        self.subject = lesson.group.subject
        self.text = lesson.homework
        self.file = lesson.h_file
        self.id = lesson.id

    @property
    def file_exists(self):
        """Show if homework task has an attached file."""
        return bool(self.file)


def get_homework(
        klass: models.Klasses,
        quarter: Union[int, None] = None,
        start_date: Union[datetime.date, None] = None,
        end_date: Union[datetime.date, None] = None,
        reverse: bool = False,
        convert: bool = True):
    """
    Get homework for a specified class. If both `start_date` and `end_date` are
    specified, search for homework in this time range. Otherwise (only `start_date`)
    get homework only for that day.

    Also you can specify `quarter` if you need to find all homework for that quarter.

    Args:
        klass: A class where the search is performed.
        quarter: A quarter's number.
        start_date: A date for which the search is performed.
        end_date: If not omitted, start_date turns into a start date
                  of time range and end_date means an end of the range
                  for which the search is performed.
        reverse: show homework list in a reversed order.
        convert: convert all the objects in a final
                 queryset into core.homework.Homework.

    Returns:
        A list of core.homework.Homework objects if convert is True.
        Otherwise, returns a QuerySet.

    Raises:
        TypeError: no quarter, start_date or end_date arguments are specified.
    """
    if not quarter and not (start_date or end_date):
        return TypeError(
            "At least one argument: quarter, start_date or end_date is expected.")
    args = [Q(homework__iregex=r'\S+') | Q(h_file__iregex=r'\S+')]
    kwargs = {
        "group__klass": klass
    }
    if quarter:
        kwargs["quarter__number"] = quarter
    if end_date is not None:
        kwargs["date__range"] = (start_date, end_date)
    elif start_date is not None:
        kwargs["date"] = start_date
    queryset = models.Lessons.objects.filter(*args, **kwargs)
    if reverse:
        queryset = queryset.order_by('-date')
    if not convert:
        return queryset
    return [Homework(i) for i in queryset]


def add_homework(
        date: datetime.date, group: int,
        homework: str = "", h_file=None) -> models.Lessons:
    """
    Add homework for a specified date.

    Args:
        date: Date for which homework is added.
        group: An id of core.models.Groups object.
        homework: Description of the task.
        h_file: File attached to a homework.

    Returns:
        A core.models.Lessons object with added homework.

    Raises:
        ValueError: date is on holidays.
    """
    quarter: int = models.Quarters.get_quarter_by_date(date)
    if quarter == 0:
        raise ValueError("Lesson's date can't be holidays time.")
    lessons = models.Lessons.objects.filter(group_id=group, date=date)
    for lesson in lessons:
        if not (lesson.homework or lesson.h_file):
            lesson.homework = homework
            lesson.h_file = h_file
            lesson.save()
            return lesson
    # Lesson with no homework wasn't found, so we are
    # going to create a new one.
    control = models.Controls.objects.get_or_create(
        name="Работа на уроке", weight=1
    )[0]
    # TODO: Fix that shit ^^^
    lesson = models.Lessons.objects.create(
        date=date, quarter=quarter,
        homework=homework, h_file=h_file,
        control=control, group=group
    )
    return lesson
