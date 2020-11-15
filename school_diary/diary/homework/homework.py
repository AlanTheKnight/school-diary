from diary import models


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
