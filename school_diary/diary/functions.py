import datetime


TERMS = (
    ((1, 7), (27, 10)),
    ((3, 11), (29, 12)),
    ((12, 1), (21, 3)),  # FIX ON PRODUCTION
    ((29, 3), (27, 5))
)


def get_quarter_by_date(datestring: str) -> int:
    """
    Returns a number of a quarter by the date stamp string.
    If quarter does not exit, return 0 instead.
    """
    converted_date = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    year = converted_date.year
    for i in range(0, 4):
        start = datetime.date(year, TERMS[i][0][1], TERMS[i][0][0])
        end = datetime.date(year, TERMS[i][1][1], TERMS[i][1][0])
        if start <= converted_date <= end:
            return i + 1
    else:
        return 0


def check_if_teacher_has_class(teacher):
    if teacher.grades_set.all():
        return True
    return False


def get_needed_mark(average):
    pass
