from diary import models
import utils
import datetime
from typing import List
from django.db.models import Q
from .homework import Homework


def add_homework(cleaned_data: dict, group: int) -> models.Lessons:
    """
    Add homework to specified date.

    Args:
        cleaned_data - cleaned_data attribute
        of diary.forms.HomeworkForm
        group - current id of diary.models.Groups
    """
    date = cleaned_data.get('date')
    quarter: int = utils.get_quarter_by_date(date)
    homework: str = cleaned_data.get('homework', '')
    h_file = cleaned_data.get('h_file')
    if quarter == 0:
        raise ValueError("Lesson's date can't be on holidays.")
    lessons = models.Lessons.objects.filter(
        group_id=group,
        date=date
        )
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
    lesson = models.Lessons.objects.create(
        date=date, quarter=quarter,
        homework=cleaned_data.get('homework', ''),
        h_file=cleaned_data.get('h_file'),
        control=control, group_id=group
    )
    return lesson


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
            group__grade=grade,
            date__range=(start_date, end_date))
    else:
        queryset = models.Lessons.objects.filter(
            Q(homework__iregex=r'\S+') | Q(h_file__iregex=r'\S+'),
            group__grade=grade, date=start_date)
    return [Homework(i) for i in queryset]
