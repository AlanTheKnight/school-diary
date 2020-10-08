import datetime
from typing import List
from django.db.models import Q
from diary import models
from .homework import Homework


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
