from functools import reduce
from diary.models import Marks
from django.db.models import Q


def save_marks(data, group):
    """
    Preforms create/update/delete operations on marks passed as post data
    to this request.

    Post data format:
        [
            {
                student: <id>,
                lesson: <id>,
                value: <number>,
            },
        ]

    Returns:
        Dictionary with count of how many elements have been
        created/deleted/updated.
    """
    marks = Marks.objects.select_for_update().filter(lesson__group_id=group.id)

    marks_in_db = {
        (m.student_id, m.lesson_id): m for m in marks
    }

    to_update = []
    to_create = []
    to_delete = []
    for mark in data:
        key = (mark['student'], mark['lesson'])
        if mark['value'] == "" and key in marks_in_db:
            to_delete.append(Q(id=marks_in_db[key].id))
        elif mark['value'] != "" and key not in marks_in_db:
            to_create.append(
                Marks(student=mark['student'], lesson=mark['lesson'], amount=int(mark['value']))
            )
        else:
            m = marks_in_db[key]
            m.amount = int(mark['value'])
            to_update.append(m)

    Marks.objects.bulk_create(to_create)
    Marks.objects.bulk_update(to_update, ['amount'])
    if len(to_delete != 0):
        Marks.objects.filter(reduce(lambda x, y: x | y, to_delete)).delete()

    data = {
        'update': len(to_update),
        'create': len(to_create),
        'delete': len(to_delete),
    }
    return data
