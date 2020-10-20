from diary import models
import utils


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
